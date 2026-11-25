import { useCallback, useEffect, useRef, useState } from "react";
import {
  Alert,
  Box,
  Chip,
  CircularProgress,
  Drawer,
  IconButton,
  Tooltip,
  Typography,
  useMediaQuery,
  useTheme,
} from "@mui/material";
import {
  AddRounded,
  MenuRounded,
  SmartToyOutlined,
  ViewSidebarOutlined,
} from "@mui/icons-material";
import Sidebar from "./Sidebar";
import MessageBubble from "./MessageBubble";
import ToolGroup from "./ToolGroup";
import Composer from "./Composer";
import {
  createChat,
  deleteChat,
  getChat,
  getChats,
  sendMessage,
  updateChat,
} from "../lib/chat";
import type { Chat, Message } from "../lib/types";

const DRAWER_WIDTH = 300;

const STARTER_PROMPTS = [
  "Check home temperature & humidity",
  "How's the weather in NYC?",
  "Toggle desk LED status",
];

type RenderBlock =
  | { kind: "message"; message: Message }
  | { kind: "tools"; tools: Message[]; key: string };

function groupMessages(messages: Message[]): RenderBlock[] {
  const blocks: RenderBlock[] = [];
  let toolBuf: Message[] = [];

  const flushTools = () => {
    if (toolBuf.length === 0) return;
    blocks.push({
      kind: "tools",
      tools: toolBuf,
      key: toolBuf.map((t) => t.id).join("-"),
    });
    toolBuf = [];
  };

  for (const m of messages) {
    if (m.role === "tool") {
      toolBuf.push(m);
    } else {
      flushTools();
      blocks.push({ kind: "message", message: m });
    }
  }
  flushTools();
  return blocks;
}

export default function ChatApp() {
  const theme = useTheme();
  const isDesktop = useMediaQuery(theme.breakpoints.up("md"));

  const [chats, setChats] = useState<Chat[]>([]);
  const [activeChatId, setActiveChatId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");

  const [loadingChats, setLoadingChats] = useState(true);
  const [loadingMessages, setLoadingMessages] = useState(false);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);

  const bottomRef = useRef<HTMLDivElement | null>(null);
  const loadSeqRef = useRef(0);

  const isEmptyNewChat = !loadingMessages && messages.length === 0;

  const scrollToBottom = useCallback(() => {
    requestAnimationFrame(() => {
      bottomRef.current?.scrollIntoView({ behavior: "smooth" });
    });
  }, []);

  const refreshChats = useCallback(async () => {
    const data = await getChats();
    const sorted = [...data].sort(
      (a, b) =>
        new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime(),
    );
    setChats(sorted);
    return sorted;
  }, []);

  const loadChat = useCallback(async (chatId: string) => {
    const seq = ++loadSeqRef.current;
    setActiveChatId(chatId);
    setMessages([]);
    setLoadingMessages(true);

    try {
      const chat = await getChat(chatId);
      if (loadSeqRef.current === seq) {
        setMessages(chat.messages ?? []);
      }
    } catch {
      if (loadSeqRef.current === seq) {
        setError("Could not load this conversation.");
      }
    } finally {
      if (loadSeqRef.current === seq) {
        setLoadingMessages(false);
      }
    }
  }, []);

  useEffect(() => {
    let cancelled = false;

    async function boot() {
      try {
        await refreshChats();
      } catch {
        if (!cancelled) {
          setError("Could not reach Rachel API. Check backend URL and CORS.");
        }
      } finally {
        if (!cancelled) {
          setLoadingChats(false);
        }
      }
    }

    void boot();
    return () => {
      cancelled = true;
    };
  }, [refreshChats]);

  useEffect(() => {
    scrollToBottom();
  }, [messages, sending, scrollToBottom]);

  function selectChat(chatId: string) {
    setMobileOpen(false);
    setError(null);
    if (chatId === activeChatId) return;
    void loadChat(chatId);
  }

  function handleNewChat() {
    loadSeqRef.current += 1;
    setError(null);
    setMobileOpen(false);
    setActiveChatId(null);
    setMessages([]);
    setInput("");
    setLoadingMessages(false);
  }

  async function handleDelete(chatId: string) {
    setError(null);
    try {
      await deleteChat(chatId);
      const remaining = await refreshChats();

      if (activeChatId === chatId) {
        if (remaining.length > 0) {
          await loadChat(remaining[0].id);
        } else {
          handleNewChat();
        }
      }
    } catch {
      setError("Could not delete this conversation.");
    }
  }

  async function handleRename(chatId: string, title: string) {
    setError(null);
    try {
      await updateChat(chatId, { title });
      await refreshChats();
    } catch {
      setError("Could not rename this conversation.");
    }
  }

  async function handleSend() {
    const content = input.trim();
    if (!content || sending) return;

    setError(null);
    setSending(true);
    setInput("");

    const tempId = `temp-${Date.now()}`;
    const now = new Date().toISOString();
    const optimistic: Message = {
      id: tempId,
      chat_id: activeChatId ?? "",
      content,
      role: "user",
      tool_name: null,
      created_at: now,
      updated_at: now,
    };
    setMessages((prev) => [...prev, optimistic]);

    try {
      let chatId = activeChatId;

      if (!chatId) {
        const chat = await createChat({
          title: content.slice(0, 48) || "New chat",
        });
        chatId = chat.id;
        setActiveChatId(chatId);
        setMessages((prev) =>
          prev.map((m) => (m.id === tempId ? { ...m, chat_id: chatId! } : m)),
        );
      }

      const newMessages = await sendMessage(chatId, { content });

      setMessages((prev) => {
        const withoutTemp = prev.filter((m) => m.id !== tempId);
        const existingIds = new Set(withoutTemp.map((m) => m.id));
        const toAdd = newMessages.filter((m) => !existingIds.has(m.id));
        return [...withoutTemp, ...toAdd];
      });

      await refreshChats();
    } catch {
      setMessages((prev) => prev.filter((m) => m.id !== tempId));
      setInput(content);
      setError("Sending failed. Check the backend and try again.");
    } finally {
      setSending(false);
    }
  }

  const activeTitle =
    chats.find((c) => c.id === activeChatId)?.title ?? "Rachel";

  const sidebar = (
    <Sidebar
      chats={chats}
      activeChatId={activeChatId}
      loading={loadingChats}
      canCollapse={isDesktop}
      onCollapse={() => setSidebarOpen(false)}
      onSelect={selectChat}
      onNew={handleNewChat}
      onDelete={(id) => void handleDelete(id)}
      onRename={(id, title) => void handleRename(id, title)}
    />
  );

  return (
    <Box
      sx={{
        display: "flex",
        height: "100dvh",
        width: "100%",
        overflow: "hidden",
        bgcolor: "background.default",
        position: "relative",
      }}
    >
      {/* Collapsible desktop sidebar */}
      {isDesktop && (
        <Box
          sx={{
            width: sidebarOpen ? DRAWER_WIDTH : 0,
            flexShrink: 0,
            overflow: "hidden",
            borderRight: sidebarOpen ? "1px solid" : "none",
            borderColor: "divider",
            height: "100%",
            transition: "width 220ms cubic-bezier(0.2, 0, 0, 1)",
          }}
        >
          <Box sx={{ width: DRAWER_WIDTH, height: "100%" }}>{sidebar}</Box>
        </Box>
      )}

      {/* Mobile drawer */}
      {!isDesktop && (
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={() => setMobileOpen(false)}
          ModalProps={{ keepMounted: true }}
          sx={{
            "& .MuiDrawer-paper": {
              width: DRAWER_WIDTH,
              boxSizing: "border-box",
            },
          }}
        >
          {sidebar}
        </Drawer>
      )}

      {/* Main chat column */}
      <Box
        sx={{
          flex: 1,
          minWidth: 0,
          display: "flex",
          flexDirection: "column",
          height: "100%",
          position: "relative",
          backgroundImage: (t) =>
            t.palette.mode === "dark"
              ? "radial-gradient(ellipse 65% 42% at 50% 18%, rgba(107, 207, 154, 0.08), transparent 72%)"
              : "radial-gradient(ellipse 65% 42% at 50% 18%, rgba(27, 122, 74, 0.06), transparent 72%)",
        }}
      >
        {/* Mobile top bar */}
        {!isDesktop && (
          <Box
            sx={{
              display: "flex",
              alignItems: "center",
              gap: 1.5,
              px: 2,
              py: 1.25,
              minHeight: 56,
              borderBottom: "1px solid",
              borderColor: "divider",
              bgcolor: "background.paper",
            }}
          >
            <IconButton
              onClick={() => setMobileOpen(true)}
              aria-label="Open chats"
              sx={{
                ml: 0.25,
                width: 40,
                height: 40,
              }}
            >
              <MenuRounded />
            </IconButton>
            <Typography noWrap sx={{ flex: 1, pr: 1, fontWeight: 600 }}>
              {activeTitle}
            </Typography>
          </Box>
        )}

        {/* Floating desktop controls when sidebar is collapsed */}
        {isDesktop && !sidebarOpen && (
          <Box
            sx={{
              position: "absolute",
              top: 14,
              left: 14,
              zIndex: 10,
              display: "flex",
              alignItems: "center",
              gap: 0.5,
              p: 0.35,
              borderRadius: 1.5,
              bgcolor: "background.paper",
              border: "1px solid",
              borderColor: "divider",
            }}
          >
            <Tooltip title="Expand sidebar">
              <IconButton
                size="small"
                onClick={() => setSidebarOpen(true)}
                aria-label="Expand sidebar"
                sx={{
                  color: "text.secondary",
                  "&:hover": {
                    color: "primary.main",
                    bgcolor: "action.hover",
                  },
                }}
              >
                <ViewSidebarOutlined fontSize="small" />
              </IconButton>
            </Tooltip>
            <Tooltip title="New chat">
              <IconButton
                size="small"
                onClick={handleNewChat}
                aria-label="New chat"
                sx={{
                  color: "text.secondary",
                  "&:hover": {
                    color: "primary.main",
                    bgcolor: "action.hover",
                  },
                }}
              >
                <AddRounded fontSize="small" />
              </IconButton>
            </Tooltip>
          </Box>
        )}

        {error && (
          <Alert
            severity="error"
            onClose={() => setError(null)}
            sx={{ mx: 2, mt: 2, borderRadius: 2.5 }}
          >
            {error}
          </Alert>
        )}

        {loadingMessages ? (
          <Box
            sx={{
              flex: 1,
              display: "grid",
              placeItems: "center",
            }}
          >
            <CircularProgress size={28} />
          </Box>
        ) : isEmptyNewChat ? (
          /* Centered Gemini-style new chat layout */
          <Box
            sx={{
              flex: 1,
              overflowY: "auto",
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
              px: { xs: 1.5, sm: 3 },
              py: 4,
            }}
          >
            <Box
              sx={{
                width: "100%",
                maxWidth: 740,
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                gap: 2.25,
              }}
            >
              <Box
                sx={{
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  gap: 1.25,
                  textAlign: "center",
                }}
              >
                <Box
                  sx={{
                    width: 60,
                    height: 60,
                    borderRadius: 3,
                    display: "grid",
                    placeItems: "center",
                    bgcolor: "action.selected",
                    border: "1px solid",
                    borderColor: "divider",
                    color: "primary.main",
                  }}
                >
                  <SmartToyOutlined sx={{ fontSize: 30 }} />
                </Box>
                <Typography
                  variant="h5"
                  sx={{
                    fontWeight: 700,
                    fontSize: { xs: "1.45rem", sm: "1.85rem" },
                  }}
                >
                  Where should we start?
                </Typography>
                <Typography
                  variant="body2"
                  color="text.secondary"
                  sx={{ maxWidth: 420 }}
                >
                  Ask Rachel about home sensors, control devices, or check the
                  weather.
                </Typography>
              </Box>

              <Box sx={{ width: "100%" }}>
                <Composer
                  value={input}
                  sending={sending}
                  onChange={setInput}
                  onSend={() => void handleSend()}
                />
              </Box>

              <Box
                sx={{
                  display: "flex",
                  flexWrap: "wrap",
                  justifyContent: "center",
                  gap: 1,
                  maxWidth: 640,
                }}
              >
                {STARTER_PROMPTS.map((prompt) => (
                  <Chip
                    key={prompt}
                    label={prompt}
                    variant="outlined"
                    clickable
                    onClick={() => setInput(prompt)}
                    sx={{
                      borderRadius: 1.5,
                      borderColor: "divider",
                      bgcolor: "background.paper",
                      color: "text.secondary",
                      fontWeight: 500,
                      transition:
                        "border-color 140ms ease, color 140ms ease, background-color 140ms ease, transform 120ms ease",
                      "&:hover": {
                        borderColor: "primary.main",
                        color: "primary.main",
                        bgcolor: "action.hover",
                        transform: "translateY(-1px)",
                      },
                    }}
                  />
                ))}
              </Box>
            </Box>
          </Box>
        ) : (
          /* Active conversation view + bottom-docked composer */
          <>
            <Box
              sx={{
                flex: 1,
                overflowY: "auto",
                px: { xs: 1.5, sm: 3 },
                py: 3,
              }}
            >
              <Box
                sx={{
                  maxWidth: 800,
                  mx: "auto",
                  display: "flex",
                  flexDirection: "column",
                  gap: 1.75,
                }}
              >
                {groupMessages(messages).map((block) =>
                  block.kind === "tools" ? (
                    <ToolGroup key={block.key} tools={block.tools} />
                  ) : (
                    <MessageBubble
                      key={block.message.id}
                      message={block.message}
                    />
                  ),
                )}

                {sending && (
                  <Box
                    sx={{
                      display: "flex",
                      alignItems: "center",
                      gap: 1,
                      pl: 0.5,
                    }}
                  >
                    <CircularProgress size={14} />
                    <Typography variant="caption" color="text.secondary">
                      Rachel is thinking…
                    </Typography>
                  </Box>
                )}

                <div ref={bottomRef} />
              </Box>
            </Box>

            <Box sx={{ maxWidth: 800, width: "100%", mx: "auto" }}>
              <Composer
                value={input}
                sending={sending}
                onChange={setInput}
                onSend={() => void handleSend()}
              />
            </Box>
          </>
        )}
      </Box>
    </Box>
  );
}

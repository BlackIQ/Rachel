import { useState, type ReactNode } from "react";
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Box, IconButton, Paper, Tooltip } from "@mui/material";
import { CheckRounded, ContentCopyRounded } from "@mui/icons-material";
import ThinkingBlock from "./ThinkingBlock";
import { markdownSx } from "../lib/markdownSx";
import type { Message } from "../lib/types";

function extractText(node: ReactNode): string {
  if (node == null || typeof node === "boolean") return "";
  if (typeof node === "string" || typeof node === "number") return String(node);
  if (Array.isArray(node)) return node.map(extractText).join("");
  if (typeof node === "object" && "props" in node) {
    return extractText(
      (node as { props?: { children?: ReactNode } }).props?.children,
    );
  }
  return "";
}

function CodeBlock({
  children,
  inverted,
}: {
  children: ReactNode;
  inverted: boolean;
}) {
  const [copied, setCopied] = useState(false);

  async function handleCopy() {
    const raw = extractText(children).replace(/\n$/, "");
    if (!raw) return;
    try {
      await navigator.clipboard.writeText(raw);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1600);
    } catch {
      // Ignore clipboard permission errors in restricted contexts
    }
  }

  return (
    <Box sx={{ position: "relative", my: 0.8 }}>
      <Tooltip title={copied ? "Copied" : "Copy code"}>
        <IconButton
          size="small"
          onClick={() => void handleCopy()}
          aria-label="Copy code"
          sx={{
            position: "absolute",
            top: 6,
            right: 6,
            zIndex: 1,
            width: 26,
            height: 26,
            bgcolor: inverted ? "rgba(0, 0, 0, 0.28)" : "background.paper",
            border: "1px solid",
            borderColor: inverted ? "rgba(255, 255, 255, 0.18)" : "divider",
            color: copied ? "primary.main" : "text.secondary",
            "&:hover": {
              color: "text.primary",
              bgcolor: inverted ? "rgba(0, 0, 0, 0.42)" : "action.hover",
            },
          }}
        >
          {copied ? (
            <CheckRounded sx={{ fontSize: 14 }} />
          ) : (
            <ContentCopyRounded sx={{ fontSize: 13 }} />
          )}
        </IconButton>
      </Tooltip>

      <Box
        component="pre"
        sx={{
          m: 0,
          p: 1.2,
          pr: 4.5,
          borderRadius: 1.25,
          overflowX: "auto",
          bgcolor: inverted ? "rgba(0, 0, 0, 0.24)" : "action.hover",
          border: "1px solid",
          borderColor: inverted ? "rgba(255, 255, 255, 0.14)" : "divider",
          "& code": {
            fontFamily:
              'ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace',
            fontSize: "0.825rem",
            lineHeight: 1.52,
            bgcolor: "transparent !important",
            border: "0 !important",
            p: "0 !important",
          },
        }}
      >
        {children}
      </Box>
    </Box>
  );
}

export default function MessageBubble({ message }: { message: Message }) {
  if (message.role === "tool") return null;

  const isUser = message.role === "user";
  const isAssistant = message.role === "assistant";
  const content = message.content ?? "";
  const thinking = message.thinking?.trim() ?? "";

  const hasContent = content.trim().length > 0;
  const hasThinking = thinking.length > 0;

  if (!hasContent && !hasThinking) return null;

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        alignItems: isUser ? "flex-end" : "flex-start",
        gap: 1.15,
      }}
    >
      {hasThinking && <ThinkingBlock thinking={thinking} />}

      {hasContent && (
        <Paper
          elevation={0}
          sx={{
            maxWidth: { xs: "92%", sm: "76%" },
            px: 1.85,
            py: 1.25,
            borderRadius: 1.75,
            bgcolor: isUser ? "primary.main" : "background.paper",
            color: isUser ? "primary.contrastText" : "text.primary",
            border: isAssistant ? "1px solid" : "none",
            borderColor: "divider",
            boxShadow: isAssistant
              ? "0 1px 2px rgba(0, 0, 0, 0.08)"
              : "0 2px 8px rgba(27, 122, 74, 0.16)",
          }}
        >
          <Box
            dir="auto"
            sx={{
              ...markdownSx,
              ...(isUser && {
                "& code:not(pre code)": {
                  bgcolor: "rgba(255, 255, 255, 0.18)",
                  borderColor: "rgba(255, 255, 255, 0.25)",
                },
                "& blockquote": {
                  borderColor: "currentColor",
                  color: "inherit",
                  opacity: 0.92,
                },
                "& a": {
                  color: "inherit",
                },
                "& th, & td": {
                  borderColor: "rgba(255, 255, 255, 0.28)",
                },
                "& th": {
                  bgcolor: "rgba(255, 255, 255, 0.12)",
                },
              }),
            }}
          >
            <Markdown
              remarkPlugins={[remarkGfm]}
              components={{
                pre: ({ children }) => (
                  <CodeBlock inverted={isUser}>{children}</CodeBlock>
                ),
              }}
            >
              {content}
            </Markdown>
          </Box>
        </Paper>
      )}
    </Box>
  );
}

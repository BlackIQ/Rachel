import { useState } from "react";
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Box, Collapse, Paper, Typography } from "@mui/material";
import { ExpandMoreRounded, PsychologyAltOutlined } from "@mui/icons-material";
import type { Message } from "../lib/types";

export default function MessageBubble({ message }: { message: Message }) {
  const [thinkingOpen, setThinkingOpen] = useState(false);

  if (message.role === "tool") return null;

  const isUser = message.role === "user";
  const isAssistant = message.role === "assistant";
  const thinkingText = message.thinking?.trim() ?? "";
  const hasThinking = thinkingText.length > 0;

  return (
    <Box
      sx={{
        display: "flex",
        justifyContent: isUser ? "flex-end" : "flex-start",
      }}
    >
      <Paper
        elevation={0}
        sx={{
          maxWidth: { xs: "92%", sm: "75%" },
          px: 1.75,
          py: 1.2,
          borderRadius: 1.5,
          bgcolor: isUser ? "primary.main" : "background.paper",
          color: isUser ? "primary.contrastText" : "text.primary",
          border: isAssistant ? "1px solid" : "none",
          borderColor: "divider",
        }}
      >
        {hasThinking && (
          <Box sx={{ mb: 0.75 }}>
            <Box
              component="button"
              type="button"
              onClick={() => setThinkingOpen((prev) => !prev)}
              aria-expanded={thinkingOpen}
              sx={{
                all: "unset",
                cursor: "pointer",
                display: "inline-flex",
                alignItems: "center",
                gap: 0.6,
                px: 0.65,
                py: 0.25,
                borderRadius: 1,
                color: isUser ? "inherit" : "text.secondary",
                opacity: isUser ? 0.85 : 1,
                transition: "color 120ms ease, background-color 120ms ease",
                "&:hover": {
                  color: isUser ? "inherit" : "text.primary",
                  bgcolor: isUser
                    ? "rgba(255, 255, 255, 0.12)"
                    : "action.hover",
                },
              }}
            >
              <PsychologyAltOutlined sx={{ fontSize: 15, opacity: 0.85 }} />
              <Typography
                component="span"
                sx={{
                  fontSize: "0.75rem",
                  lineHeight: 1.4,
                  fontWeight: 500,
                }}
              >
                Thinking
              </Typography>
              <ExpandMoreRounded
                sx={{
                  fontSize: 16,
                  opacity: 0.75,
                  transform: thinkingOpen ? "rotate(180deg)" : "none",
                  transition: "transform 150ms ease",
                }}
              />
            </Box>

            <Collapse in={thinkingOpen}>
              <Box
                dir="auto"
                sx={{
                  mt: 0.5,
                  ml: 0.5,
                  pl: 1.25,
                  pr: 0.5,
                  py: 0.5,
                  borderLeft: "2px solid",
                  borderColor: isUser ? "currentColor" : "divider",
                  opacity: isUser ? 0.9 : 1,
                }}
              >
                <Typography
                  component="div"
                  sx={{
                    fontFamily:
                      'ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace',
                    fontSize: "0.75rem",
                    lineHeight: 1.5,
                    color: isUser ? "inherit" : "text.secondary",
                    whiteSpace: "pre-wrap",
                    overflowWrap: "anywhere",
                  }}
                >
                  {thinkingText}
                </Typography>
              </Box>
            </Collapse>
          </Box>
        )}

        <Box
          dir="auto"
          sx={{
            fontSize: "0.925rem",
            lineHeight: 1.65,
            overflowWrap: "anywhere",
            "& > :first-of-type": { mt: 0 },
            "& > :last-child": { mb: 0 },
            "& p": { my: 0.6 },
            "& h1, & h2, & h3, & h4": {
              mt: 1.25,
              mb: 0.5,
              fontWeight: 700,
              lineHeight: 1.35,
            },
            "& h1": { fontSize: "1.25rem" },
            "& h2": { fontSize: "1.1rem" },
            "& h3": { fontSize: "1rem" },
            "& ul, & ol": {
              my: 0.6,
              pl: 2.5,
            },
            "& li": { my: 0.25 },
            "& code:not(pre code)": {
              fontFamily:
                'ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace',
              fontSize: "0.85em",
              px: 0.55,
              py: 0.15,
              borderRadius: 0.75,
              bgcolor: isUser ? "rgba(255, 255, 255, 0.16)" : "action.hover",
            },
            "& pre": {
              my: 0.85,
              p: 1.25,
              borderRadius: 1,
              overflowX: "auto",
              bgcolor: isUser ? "rgba(0, 0, 0, 0.22)" : "action.hover",
              border: "1px solid",
              borderColor: isUser ? "transparent" : "divider",
            },
            "& pre code": {
              fontFamily:
                'ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace',
              fontSize: "0.825rem",
              lineHeight: 1.5,
              background: "transparent",
              padding: 0,
            },
            "& blockquote": {
              my: 0.75,
              pl: 1.25,
              ml: 0.25,
              borderLeft: "2px solid",
              borderColor: isUser ? "currentColor" : "primary.main",
              opacity: 0.9,
            },
            "& a": {
              color: isUser ? "inherit" : "primary.main",
              textDecoration: "underline",
              textUnderlineOffset: 2,
            },
            "& table": {
              width: "100%",
              borderCollapse: "collapse",
              my: 0.85,
              fontSize: "0.85rem",
            },
            "& th, & td": {
              border: "1px solid",
              borderColor: isUser ? "rgba(255,255,255,0.25)" : "divider",
              px: 1,
              py: 0.5,
              textAlign: "start",
            },
            "& th": {
              fontWeight: 600,
              bgcolor: isUser ? "rgba(255,255,255,0.1)" : "action.hover",
            },
            "& hr": {
              border: 0,
              borderTop: "1px solid",
              borderColor: "divider",
              my: 1,
            },
          }}
        >
          <Markdown remarkPlugins={[remarkGfm]}>{message.content}</Markdown>
        </Box>
      </Paper>
    </Box>
  );
}

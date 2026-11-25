import { useState } from "react";
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Box, Collapse, Paper, Typography } from "@mui/material";
import { ExpandMoreRounded, PsychologyAltOutlined } from "@mui/icons-material";
import type { Message } from "../lib/types";

const markdownSx = {
  fontSize: "0.925rem",
  lineHeight: 1.65,
  overflowWrap: "anywhere" as const,
  "& > :first-of-type": { mt: 0 },
  "& > :last-child": { mb: 0 },
  "& p": { my: 0.5 },
  "& h1, & h2, & h3, & h4": {
    mt: 1.1,
    mb: 0.4,
    fontWeight: 700,
    lineHeight: 1.35,
  },
  "& h1": { fontSize: "1.2rem" },
  "& h2": { fontSize: "1.05rem" },
  "& h3": { fontSize: "0.975rem" },
  "& ul, & ol": {
    my: 0.5,
    pl: 2.25,
  },
  "& li": { my: 0.2 },
  "& code:not(pre code)": {
    fontFamily:
      'ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace',
    fontSize: "0.84em",
    px: 0.5,
    py: 0.1,
    borderRadius: 0.75,
    bgcolor: "action.hover",
  },
  "& pre": {
    my: 0.75,
    p: 1.15,
    borderRadius: 1,
    overflowX: "auto" as const,
    bgcolor: "action.hover",
    border: "1px solid",
    borderColor: "divider",
  },
  "& pre code": {
    fontFamily:
      'ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace',
    fontSize: "0.825rem",
    lineHeight: 1.5,
    bgcolor: "transparent !important",
    p: "0 !important",
  },
  "& blockquote": {
    my: 0.6,
    pl: 1.2,
    ml: 0.2,
    borderLeft: "2px solid",
    borderColor: "primary.main",
    color: "text.secondary",
  },
  "& a": {
    color: "primary.main",
    textDecoration: "underline",
    textUnderlineOffset: 2,
  },
  "& table": {
    width: "100%",
    borderCollapse: "collapse" as const,
    my: 0.75,
    fontSize: "0.85rem",
  },
  "& th, & td": {
    border: "1px solid",
    borderColor: "divider",
    px: 1,
    py: 0.45,
    textAlign: "start" as const,
  },
  "& th": {
    fontWeight: 600,
    bgcolor: "action.hover",
  },
  "& hr": {
    border: 0,
    borderTop: "1px solid",
    borderColor: "divider",
    my: 0.85,
  },
};

function ThinkingSection({ thinking }: { thinking: string }) {
  const [open, setOpen] = useState(false);

  return (
    <Box sx={{ maxWidth: { xs: "95%", sm: "80%" } }}>
      <Box
        component="button"
        type="button"
        onClick={() => setOpen((prev) => !prev)}
        aria-expanded={open}
        sx={{
          all: "unset",
          cursor: "pointer",
          display: "inline-flex",
          alignItems: "center",
          gap: 0.6,
          px: 0.75,
          py: 0.35,
          borderRadius: 1,
          color: "text.secondary",
          transition: "color 120ms ease, background-color 120ms ease",
          "&:hover": {
            color: "text.primary",
            bgcolor: "action.hover",
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
            transform: open ? "rotate(180deg)" : "none",
            transition: "transform 150ms ease",
          }}
        />
      </Box>

      <Collapse in={open}>
        <Box
          dir="auto"
          sx={{
            mt: 0.5,
            ml: 0.5,
            pl: 1.25,
            pr: 0.5,
            py: 0.4,
            borderLeft: "2px solid",
            borderColor: "divider",
            color: "text.secondary",
            ...markdownSx,
            fontSize: "0.8rem",
            lineHeight: 1.5,
          }}
        >
          <Markdown remarkPlugins={[remarkGfm]}>{thinking}</Markdown>
        </Box>
      </Collapse>
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
        gap: 1.25,
      }}
    >
      {hasThinking && <ThinkingSection thinking={thinking} />}

      {hasContent && (
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
          <Box
            dir="auto"
            sx={{
              ...markdownSx,
              ...(isUser && {
                "& code:not(pre code)": {
                  bgcolor: "rgba(255, 255, 255, 0.16)",
                },
                "& pre": {
                  bgcolor: "rgba(0, 0, 0, 0.22)",
                  borderColor: "transparent",
                },
                "& pre code": {
                  bgcolor: "transparent !important",
                },
                "& blockquote": {
                  borderColor: "currentColor",
                  color: "inherit",
                  opacity: 0.9,
                },
                "& a": {
                  color: "inherit",
                },
                "& th, & td": {
                  borderColor: "rgba(255, 255, 255, 0.25)",
                },
                "& th": {
                  bgcolor: "rgba(255, 255, 255, 0.1)",
                },
              }),
            }}
          >
            <Markdown remarkPlugins={[remarkGfm]}>{content}</Markdown>
          </Box>
        </Paper>
      )}
    </Box>
  );
}

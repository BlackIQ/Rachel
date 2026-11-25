import { useState } from "react";
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Box, Collapse, Typography } from "@mui/material";
import { ExpandMoreRounded, PsychologyAltOutlined } from "@mui/icons-material";
import { markdownSx } from "../lib/markdownSx";

type Props = {
  thinking: string;
  label?: string;
  defaultOpen?: boolean;
};

export default function ThinkingBlock({
  thinking,
  label = "Thinking",
  defaultOpen = false,
}: Props) {
  const [open, setOpen] = useState(defaultOpen);
  const trimmed = thinking.trim();

  if (!trimmed) return null;

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
          "&:focus-visible": {
            outline: "2px solid",
            outlineColor: "primary.main",
            outlineOffset: 1,
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
          {label}
        </Typography>
        <ExpandMoreRounded
          sx={{
            fontSize: 16,
            opacity: 0.7,
            transform: open ? "rotate(180deg)" : "none",
            transition: "transform 150ms ease",
          }}
        />
      </Box>

      <Collapse in={open}>
        <Box
          dir="auto"
          sx={{
            mt: 0.65,
            ml: 0.5,
            pl: 1.25,
            borderLeft: "2px solid",
            borderColor: "divider",
            color: "text.secondary",
            ...markdownSx,
            fontSize: "0.75rem",
            lineHeight: 1.45,
            "& p": { my: 0.35 },
            "& ul, & ol": { my: 0.35, pl: 2 },
            "& li": { my: 0.15 },
            "& code:not(pre code)": {
              fontSize: "0.725rem",
              px: 0.45,
              py: 0.05,
              border: "none",
            },
          }}
        >
          <Markdown remarkPlugins={[remarkGfm]}>{trimmed}</Markdown>
        </Box>
      </Collapse>
    </Box>
  );
}

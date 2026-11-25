import type { SxProps, Theme } from "@mui/material";

export const markdownSx: SxProps<Theme> = {
  fontSize: "0.925rem",
  lineHeight: 1.65,
  overflowWrap: "anywhere",
  "& > :first-of-type": { mt: 0 },
  "& > :last-child": { mb: 0 },
  "& p": { my: 0.5 },
  "& h1, & h2, & h3, & h4": {
    mt: 1.15,
    mb: 0.4,
    fontWeight: 700,
    lineHeight: 1.35,
    letterSpacing: "-0.01em",
  },
  "& h1": { fontSize: "1.22rem" },
  "& h2": { fontSize: "1.06rem" },
  "& h3": { fontSize: "0.975rem" },
  "& ul, & ol": {
    my: 0.55,
    pl: 2.35,
  },
  "& li": { my: 0.22 },
  "& code:not(pre code)": {
    fontFamily:
      'ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace',
    fontSize: "0.84em",
    px: 0.55,
    py: 0.12,
    borderRadius: 0.75,
    bgcolor: "action.hover",
    border: "1px solid",
    borderColor: "divider",
  },
  "& pre": {
    my: 0.8,
    p: 1.2,
    borderRadius: 1.25,
    overflowX: "auto",
    bgcolor: "action.hover",
    border: "1px solid",
    borderColor: "divider",
  },
  "& pre code": {
    fontFamily:
      'ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace',
    fontSize: "0.825rem",
    lineHeight: 1.52,
    bgcolor: "transparent !important",
    border: "0 !important",
    p: "0 !important",
  },
  "& blockquote": {
    my: 0.65,
    pl: 1.25,
    ml: 0.2,
    borderLeft: "2.5px solid",
    borderColor: "primary.main",
    color: "text.secondary",
  },
  "& a": {
    color: "primary.main",
    textDecoration: "underline",
    textUnderlineOffset: 2,
    "&:hover": {
      color: "primary.light",
    },
  },
  "& table": {
    width: "100%",
    borderCollapse: "collapse",
    my: 0.8,
    fontSize: "0.85rem",
  },
  "& th, & td": {
    border: "1px solid",
    borderColor: "divider",
    px: 1,
    py: 0.5,
    textAlign: "start",
  },
  "& th": {
    fontWeight: 600,
    bgcolor: "action.hover",
  },
  "& hr": {
    border: 0,
    borderTop: "1px solid",
    borderColor: "divider",
    my: 0.9,
  },
};

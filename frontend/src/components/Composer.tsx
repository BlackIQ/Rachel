import {
  Box,
  CircularProgress,
  IconButton,
  InputBase,
  Paper,
} from "@mui/material";
import { SendRounded } from "@mui/icons-material";

type Props = {
  value: string;
  disabled?: boolean;
  sending?: boolean;
  onChange: (value: string) => void;
  onSend: () => void;
};

export default function Composer({
  value,
  disabled,
  sending,
  onChange,
  onSend,
}: Props) {
  const busy = disabled || sending;

  return (
    <Box
      sx={{
        p: { xs: 1.5, sm: 2 },
        pb: { xs: "max(12px, env(safe-area-inset-bottom))", sm: 2.5 },
        bgcolor: "background.default",
      }}
    >
      <Paper
        elevation={0}
        component="form"
        onSubmit={(e) => {
          e.preventDefault();
          onSend();
        }}
        sx={{
          display: "flex",
          alignItems: "flex-end",
          gap: 0.75,
          px: 1.1,
          py: 0.45,
          borderRadius: 1.75,
          bgcolor: "background.paper",
          border: "1px solid",
          borderColor: "divider",
          transition: "border-color 140ms ease, box-shadow 140ms ease",
          "&:focus-within": {
            borderColor: "primary.main",
            boxShadow: (theme) =>
              theme.palette.mode === "dark"
                ? "0 0 0 3px rgba(107, 207, 154, 0.14)"
                : "0 0 0 3px rgba(27, 122, 74, 0.12)",
          },
        }}
      >
        <InputBase
          fullWidth
          multiline
          maxRows={5}
          placeholder="Message Rachel…"
          value={value}
          disabled={busy}
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={(e) => {
            if (
              e.key === "Enter" &&
              !e.shiftKey &&
              !e.nativeEvent.isComposing
            ) {
              e.preventDefault();
              onSend();
            }
          }}
          inputProps={{
            dir: "auto",
            "aria-label": "Message Rachel",
          }}
          sx={{
            px: 1.1,
            py: 1,
            fontSize: "0.925rem",
            lineHeight: 1.5,
          }}
        />

        <IconButton
          type="submit"
          disabled={!value.trim() || busy}
          aria-label="Send"
          sx={{
            width: 38,
            height: 38,
            flexShrink: 0,
            mb: 0.3,
            borderRadius: 1.25,
            bgcolor: "primary.main",
            color: "primary.contrastText",
            transition: "transform 120ms ease, background-color 140ms ease",
            "&:hover": { bgcolor: "primary.dark" },
            "&:active": { transform: "scale(0.96)" },
            "&.Mui-disabled": {
              bgcolor: "action.hover",
              color: "text.disabled",
            },
          }}
        >
          {sending ? (
            <CircularProgress size={16} color="inherit" />
          ) : (
            <SendRounded sx={{ fontSize: 18 }} />
          )}
        </IconButton>
      </Paper>
    </Box>
  );
}

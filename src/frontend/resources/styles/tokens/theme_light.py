from .types import Token

THEME = {
    # ------ Background colors --------
    Token.BACKGROUND: "#FBF9FC",
    Token.BACKGROUND_DISABLED: "rgba(255,255,255, 0.6)",
    Token.BACKGROUND_BUTTON_PREVIOUS: "#E9E8EB",
    Token.BACKGROUND_BUTTON_DISABLED: "#B0B4BA",
    Token.BACKGROUND_BUTTON_HOVER: "#587528",
    Token.BACKGROUND_BUTTON_PREVIOUS_HOVER: "#e7e7e7",
    Token.COLOR_SEPARATOR_LINE: "#e8eaed",
    # ------ Text Colors ------
    Token.COLOR_TEXT_PRIMARY: "#222732",
    Token.COLOR_TEXT_SECONDARY: "#23262F",
    Token.COLOR_TEXT_MUTED: "#959697",
    Token.COLOR_TEXT_WHITE: "#ffffff",
    Token.COLOR_TEXT_DISABLED_WHITE: "#f6f8f4",
    # ------ Brand Colors (QGIS Guide) --------
    Token.COLOR_PRIMARY: "#497D29",
    Token.COLOR_DARK: "#589632",
    Token.COLOR_GREEN_LIGHT_100: "#D5E78C",
    Token.COLOR_GREEN_LIGHT_200: "#CCE46D",
    Token.COLOR_GREEN_LIGHT_300: "#C1E045",
    Token.COLOR_GREEN_LIGHT_100_OPACITY: "rgba(213, 231, 140, 0.1)",

    Token.COLOR_YELLOW_100: "#F0E971",
    Token.COLOR_YELLOW_200: "#F0E64A",
    Token.COLOR_YELLOW_100_OPACITY: "rgba(240, 230, 74, 0.1)",

    Token.COLOR_ACCENT_ORANGE_100: "#F18D36",
    Token.COLOR_ACCENT_ORANGE_200: "#EE7913",
    Token.COLOR_ACCENT_ORANGE_100_OPACITY: "rgba(241, 141, 54, 0.1)",

    Token.COLOR_BORDER_PRIMARY: "#3A6321",
    Token.COLOR_BORDER_DISABLED: "#a7b992",

    # ------ Typography --------
    Token.FONT_FAMILY: '"Segoe UI", "Helvetica Neue", "Arial"',

    Token.FONT_SIZE_TITLE: "18px",
    Token.FONT_SIZE_MEDIUM: "12px",
    Token.FONT_SIZE_BASE: "11px",
    Token.FONT_SIZE_SMALL: "10px",

    Token.FONT_WEIGHT_SEMIBOLD: "500",
    Token.FONT_WEIGHT_NORMAL: "400",

    Token.BORDER_RADIUS_PAGINATION_BUTTON: "8px",
    Token.BORDER_RADIUS_CARD: "10px",
    Token.BORDER_RADIUS_GENERAL: "6px",
    Token.BORDER_RADIUS_SCROLL: "4px",
}

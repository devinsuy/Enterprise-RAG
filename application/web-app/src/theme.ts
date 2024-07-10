import { createTheme } from '@mui/material'

const theme = createTheme({
  palette: {
    primary: {
      light: '#5a6f8c', // Light navy blue
      main: '#34495e', // Medium navy blue
      dark: '#2c3e50', // Dark navy blue
      contrastText: '#ffffff', // White for text contrast
    },
    secondary: {
      light: '#92a8d1', // Light blue-grey
      main: '#6c7a89', // Medium blue-grey
      dark: '#4a6274', // Dark blue-grey
      contrastText: '#ffffff', // White for text contrast
    },
    background: {
      default: '#f0f4f7', // Very light blue-grey for a clean look
      paper: '#ffffff', // White background for chat bubbles or cards
    },
    text: {
      primary: '#2c3e50', // Dark navy blue for primary text
      secondary: '#7f8c8d', // Medium grey for secondary text
    },
    divider: '#dfe6e9', // Light grey-blue for dividers
  },
  typography: {
    fontFamily: 'Arial, sans-serif', // Clean and modern font
    body1: {
      color: '#2c3e50', // Ensuring text uses the primary text color
    },
  },
})

export default theme

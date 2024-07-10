import React, { useState } from 'react'
import { Box, Button } from '@mui/material'
import { AppBar } from './AppBar'
import { ChatContainer } from './ChatContainer'
import { DebugPanel } from './DebugPanel'

export const MainContainer: React.FC = () => {
  const [isDebugOpen, setDebugOpen] = useState(false)

  const handleDebugOpen = () => {
    setDebugOpen(true)
  }

  const handleDebugClose = () => {
    setDebugOpen(false)
  }

  const handleClickAway = (event: React.MouseEvent<HTMLDivElement, MouseEvent>) => {
    if (isDebugOpen && !(event.target as HTMLElement).closest('.MuiDrawer-paper')) {
      setDebugOpen(false)
    }
  }

  return (
    <Box
      sx={{ display: 'flex', flexDirection: 'column', height: '100vh', backgroundColor: '#f0f0f0' }}
      onClick={handleClickAway}
    >
      <AppBar />
      <ChatContainer />
      <Button variant="contained" color="primary" onClick={handleDebugOpen} sx={{ position: 'fixed', bottom: 16, right: 16 }}>
        Open Debug Panel
      </Button>
      <DebugPanel open={isDebugOpen} onClose={handleDebugClose} />
    </Box>
  )
}

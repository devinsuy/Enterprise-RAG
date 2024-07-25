import React, { useState } from 'react'
import { Box, Button, Link, Typography } from '@mui/material'
import { AppBar } from './AppBar'
import { ChatContainer } from './ChatContainer'
import { DebugPanel } from './DebugPanel'

const introHeading = 'Scraps to Scrumptious'
const introText = `Our innovative app is designed to turn your pantry items into tasty, diet-friendly meals while reducing food waste.
We're excited for you to try it out and we'd greatly appreciate your feedback on your experience. After using the app, please take a moment to complete our survey by `
const surveyLinkText = 'clicking here'
const surveyLinkUrl = 'https://berkeley.yul1.qualtrics.com/jfe/preview/previewId/4817dcb7-d00c-4095-819c-2369cf8de90e/SV_8CzqCn6sJ8kCyPQ?Q_CHL=preview&Q_SurveyVersionID=current'
const closingText = '. Enjoy your culinary journey with us.'

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
      <Box
        sx={{
          textAlign: 'center',
          paddingTop: '30px',
          maxWidth: '45%',
          mx: 'auto' // This centers the box horizontally within its container
        }}
      >
        <Typography variant="h5" component="h2" style={{ paddingBottom: '1%' }}>
          {introHeading}
        </Typography>
        <Typography variant="body1" component="p">
          {introText}
          <Link href={surveyLinkUrl} target="_blank" rel="noopener" sx={{ color: '#0000EE' }}>
            {surveyLinkText}
          </Link>
          {closingText}
        </Typography>
      </Box>
      <ChatContainer />
      <Button variant="contained" color="primary" onClick={handleDebugOpen} sx={{ position: 'fixed', bottom: 16, right: 16 }}>
        Open Debug Panel
      </Button>
      <DebugPanel open={isDebugOpen} onClose={handleDebugClose} />
    </Box>
  )
}

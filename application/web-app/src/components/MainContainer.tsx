import React, { useState } from 'react'
import { Box, Button, Link, Typography } from '@mui/material'
import { AppBar } from './AppBar'
import { ChatContainer } from './ChatContainer'
import { DebugPanel } from './DebugPanel'
import { InfoPanel } from './InfoPanel'
import logo from '../assets/logo.jpg'

const introHeading = 'Scraps To Scrumptious'
const introText = `Our innovative app is designed to turn your pantry items into tasty, diet-friendly meals while reducing food waste.
We're excited for you to try it out and we'd greatly appreciate your feedback on your experience. After using the app, please take a moment to complete our survey by `
const surveyLinkText = 'clicking here'
const surveyLinkUrl = 'https://berkeley.qualtrics.com/jfe/form/SV_8CzqCn6sJ8kCyPQ'
const closingText = '. Enjoy your culinary journey with us.'

export const MainContainer: React.FC = () => {
  const [isDebugOpen, setDebugOpen] = useState(false)
  const [isInfoOpen, setInfoOpen] = useState(false)

  const handleDebugOpen = () => {
    setDebugOpen(true)
  }

  const handleDebugClose = () => {
    setDebugOpen(false)
  }

  const handleInfoOpen = () => {
    setInfoOpen(true)
  }

  const handleInfoClose = () => {
    setInfoOpen(false)
  }

  const handleClickAway = (event: React.MouseEvent<HTMLDivElement, MouseEvent>) => {
    if (isDebugOpen && !(event.target as HTMLElement).closest('.MuiDrawer-paper')) {
      setDebugOpen(false)
    }
    if (isInfoOpen && !(event.target as HTMLElement).closest('.MuiDrawer-paper')) {
      setInfoOpen(false)
    }
  }

  return (
    <Box
      sx={{ display: 'flex', flexDirection: 'column', height: '90vh', backgroundColor: '#f0f0f0' }}
      onClick={handleClickAway}
    >
      <Box
        sx={{
          textAlign: 'center',
          paddingTop: '30px',
          maxWidth: '45%',
          mx: 'auto', // This centers the box horizontally within its container
        }}
      >
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            paddingBottom: '3%'
          }}
        >
          {/* <Typography variant="h5" component="h2" style={{ paddingBottom: '1%' }}>
            {introHeading}
          </Typography> */}
          <Box component="img" src={logo} alt="Logo" sx={{ height: '146px', width: '239px' }} />
        </Box>
        <Typography variant="body1" component="p">
          {introText}
          <Link href={surveyLinkUrl} target="_blank" rel="noopener" sx={{ color: '#0000EE' }}>
            {surveyLinkText}
          </Link>
          {closingText}
        </Typography>
        <Button variant="contained" color="primary" onClick={handleInfoOpen} sx={{ position: 'fixed', top: 70, right: 17, marginTop: '20px', cursor: 'pointer' }}>
          Learn How To Use
        </Button>
      </Box>
      <ChatContainer />
      <Button variant="contained" color="primary" onClick={handleDebugOpen} sx={{ position: 'fixed', top: 140, right: 15 }}>
        Open Debug Panel
      </Button>
      <DebugPanel open={isDebugOpen} onClose={handleDebugClose} />
      <InfoPanel open={isInfoOpen} onClose={handleInfoClose} />
    </Box>
  )
}

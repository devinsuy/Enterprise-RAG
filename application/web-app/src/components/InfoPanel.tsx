import React from 'react'
import { Drawer, Typography, IconButton } from '@mui/material'
import CloseIcon from '@mui/icons-material/Close'

interface InfoPanelProps {
  open: boolean
  onClose: () => void
}

export const InfoPanel = ({ open, onClose }: InfoPanelProps) => {
  return (
    <Drawer anchor="right" open={open} onClose={onClose}>
      <div style={{ width: '700px', padding: 16 }}>
        <IconButton onClick={onClose}>
          <CloseIcon />
        </IconButton>
        <Typography variant="h6">How to Use</Typography>
        <Typography variant="body1" paragraph>
          Welcome to Scraps2Scrumptious! Here&apos;s how you can make the most of your culinary experience with our application:
          <ol>
            <li><strong>Start Your Query:</strong> Begin by entering your preferences, available ingredients, or a specific dish you want to prepare.</li>
            <li><strong>AI Recipe Generation:</strong> Our advanced RAG system will search through our extensive recipe database and generate a personalized recipe based on your input.</li>
            <li><strong>Customize Your Recipe:</strong> If you prefer to exclude certain ingredients or if you don&apos;t have some items at home, simply update your query. Our algorithm will adjust the recipe accordingly.</li>
            <li><strong>Use Dynamic Tuners:</strong> Click on the dynamic tuners that appear during your chat to further refine the recipe to your liking.</li>
            <li><strong>Enjoy Your Meal:</strong> Follow the detailed, step-by-step instructions provided and savor your customized culinary creation!</li>
          </ol>
        </Typography>
      </div>
    </Drawer>
  )
}

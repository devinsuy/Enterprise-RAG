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
          Welcome to Scraps2Scrumptious! Here’s how you can use our application to get the most out of your culinary experience:
          <ol>
            <li><strong>Input Your Query:</strong> Start by entering your preferences, ingredients, or any specific dish you have in mind.</li>
            <li><strong>AI Generation:</strong> Our advanced RAG system retrieves relevant information from a comprehensive recipe database and generates a customized recipe tailored to your input.</li>
            <li><strong>Fine Tuning:</strong> If you don’t like certain ingredients or don’t have them at home, enter that in the chat box. Our algorithm will adjust the recipe accordingly.</li>
            <li><strong>Enjoy Cooking:</strong> Follow the step-by-step instructions provided and enjoy your delicious meal!</li>
          </ol>
        </Typography>
      </div>
    </Drawer>
  )
}

import React from 'react'
import { Drawer, Typography, IconButton } from '@mui/material'
import CloseIcon from '@mui/icons-material/Close'

interface DebugPanelProps {
  open: boolean
  onClose: () => void
}

export const DebugPanel = ({ open, onClose }: DebugPanelProps) => {
  return (
      <Drawer anchor="right" open={open} onClose={onClose}>
        <div style={{ width: 300, padding: 16 }}>
          <IconButton onClick={onClose}>
            <CloseIcon />
          </IconButton>
          <Typography variant="h6">Debug Panel</Typography>
          {/* Add your debug information here */}
        </div>
      </Drawer>
  )
}

import React from 'react'
import { AppBar as MuiAppBar, Toolbar, Typography, Button, Tabs, Tab } from '@mui/material'
import { useChat } from '../hooks/useChat'

export const AppBar: React.FC = () => {
  const { tabs, activeTab, addTab, switchTab } = useChat()

  return (
    <MuiAppBar position="sticky">
      <Toolbar>
        <Typography variant="h6" sx={{ flexGrow: 1 }}>
            Scrumptious
        </Typography>
        <Tabs value={activeTab} onChange={(e, newValue) => { switchTab(newValue) }}>
          {tabs.map((tab) => (
            <Tab key={tab.id} label={`Thread ${tab.id + 1}`}/>
          ))}
          <Button color="inherit" onClick={addTab}>
            + New Thread
          </Button>
        </Tabs>
      </Toolbar>
    </MuiAppBar>
  )
}

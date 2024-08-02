import React from 'react'
import { AppBar as MuiAppBar, Toolbar, Typography, Button, Tabs, Tab, Box } from '@mui/material'
import { Link, useNavigate } from 'react-router-dom'
import { useChat } from '../hooks/useChat'

export const AppBar: React.FC = () => {
  const { tabs, activeTab, addTab, switchTab } = useChat()
  const navigate = useNavigate()

  return (
    <MuiAppBar position="sticky">
      <Toolbar>
        <Box sx={{ display: 'flex', alignItems: 'center', flexGrow: 1 }}>
          <Typography variant="h6" sx={{ cursor: 'pointer', paddingRight: '20px' }} onClick={() => { navigate('/') }}>
            Scraps To Scrumptious
          </Typography>
          <Tab label="Chat" component={Link} to="/" />
          <Tab label="About Us" component={Link} to="/about" />
          <Tab label="Team" component={Link} to="/team" />
          <Tab label="Technology" component={Link} to="/technology" />
        </Box>
        {window.location.pathname === '/' && <Tabs value={activeTab} onChange={(e, newValue) => { switchTab(newValue) }}>
          {tabs.map((tab) => (
            <Tab key={tab.id} label={`Thread ${tab.id + 1}`} />
          ))}
          <Button color="inherit" onClick={addTab}>
            + New Thread
          </Button>
        </Tabs>}
      </Toolbar>
    </MuiAppBar>
  )
}

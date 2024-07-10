import React from 'react'
import { List, ListItem, ListItemText } from '@mui/material'
import { useChat } from '../hooks/useChat'

export const MessageList: React.FC = () => {
  const { tabs, activeTab } = useChat()

  return (
    <List>
      {tabs[activeTab].messages.map((msg, index) => (
        <ListItem key={index} alignItems="flex-start">
          <ListItemText primary={msg.text} secondary={msg.timestamp} />
        </ListItem>
      ))}
    </List>
  )
}

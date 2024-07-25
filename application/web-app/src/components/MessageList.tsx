import React, { useEffect, useRef } from 'react'
import { List, ListItem, ListItemText } from '@mui/material'
import { useChat } from '../hooks/useChat'

export const MessageList: React.FC = () => {
  const { tabs, activeTab } = useChat()
  const listRef = useRef<HTMLUListElement>(null)

  const scrollToBottom = () => {
    if (listRef.current) {
      listRef.current.scrollTop = listRef.current.scrollHeight
    }
  }

  useEffect(() => {
    scrollToBottom()
  }, [tabs[activeTab].messages])

  return (
    <List ref={listRef} sx={{ flexGrow: 1, overflowY: 'auto' }}>
      {tabs[activeTab].messages.map((msg, i) => (
        <ListItem key={i} alignItems="flex-start" className={msg.user === 'LLM' ? 'llm-message-container' : 'user-message-container'}>
          <ListItemText primary={msg.text} secondary={msg.timestamp} className={msg.user === 'LLM' ? 'llm-message' : 'user-message'} />
        </ListItem>
      ))}
    </List>
  )
}

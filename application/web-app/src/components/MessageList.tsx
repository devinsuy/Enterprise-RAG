import React, { useEffect, useRef } from 'react'
import { List, ListItem, ListItemText, Box } from '@mui/material'
import { useChat } from '../hooks/useChat'
import { TunersList } from './TunersList'
import { MessageInput } from './MessageInput'

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
  }, [tabs, activeTab])

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '100%', position: 'relative' }}>
      <List ref={listRef} sx={{ flexGrow: 1, overflowY: 'auto' }}>
        {tabs[activeTab].messages.map((msg, i) => (
          <ListItem
            key={i}
            alignItems="flex-start"
            className={msg.user === 'LLM' ? 'llm-message-container' : 'user-message-container'}
          >
            <ListItemText
              primary={msg.text}
              secondary={msg.timestamp}
              className={msg.user === 'LLM' ? 'llm-message' : 'user-message'}
            />
          </ListItem>
        ))}
      </List>
      <Box sx={{ position: 'sticky', bottom: 0, backgroundColor: 'white', zIndex: 1, borderTop: '1px solid #ccc' }}>
        <TunersList />
        <MessageInput />
      </Box>
    </Box>
  )
}

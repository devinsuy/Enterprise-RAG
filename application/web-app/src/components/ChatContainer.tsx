import React from 'react'
import { Box } from '@mui/material'
import { MessageList } from './MessageList'
import { MessageInput } from './MessageInput'

export const ChatContainer: React.FC = () => (
  <Box sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column', backgroundColor: '#fff', margin: 10, padding: 2, borderRadius: 2, boxShadow: 1, height: '100%', maxHeight: '65vh' }}>
    <MessageList />
    <MessageInput />
  </Box>
)
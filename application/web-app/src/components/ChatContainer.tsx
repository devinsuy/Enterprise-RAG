import React from 'react'
import { Box } from '@mui/material'
import { MessageList } from './MessageList'
// import { MessageInput } from './MessageInput'
// import { TunersList } from './TunersList'

export const ChatContainer: React.FC = () => (
  <Box sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column', backgroundColor: '#fff', marginLeft: 10, marginRight: 10, marginTop: 3, padding: 2, borderRadius: 2, boxShadow: 1, height: '100%', maxHeight: '65vh' }}>
    <MessageList />
    {/* <MessageInput /> */}
  </Box>
)

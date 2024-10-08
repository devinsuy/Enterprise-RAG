import React from 'react'
import { Box } from '@mui/material'
import { MessageList } from './MessageList'
// import { MessageInput } from './MessageInput'
// import { TunersList } from './TunersList'

export const ChatContainer: React.FC = () => (
  <Box sx={{
    flexGrow: 1,
    display: 'flex',
    flexDirection: 'column',
    backgroundColor: '#fff',
    marginLeft: 'auto',
    marginRight: 'auto',
    marginTop: 3,
    padding: 2,
    borderRadius: 2,
    boxShadow: 1,
    minHeight: '60%',
    maxHeight: '60%',
    width: '100%',
    maxWidth: '60%',
    justifyContent: 'center'
  }}>
    <MessageList />
    {/* <MessageInput /> */}
  </Box>
)

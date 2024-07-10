import React, { useState } from 'react'
import { Box, TextField, Button } from '@mui/material'
import { useChat } from '../hooks/useChat'

export const MessageInput: React.FC = () => {
  const [input, setInput] = useState('')
  const { sendMessage } = useChat()

  const handleSend = () => {
    if (input.trim() !== '') {
      sendMessage(input)
      setInput('')
    }
  }

  return (
    <Box sx={{ display: 'flex', alignItems: 'center', marginTop: 2 }}>
      <TextField
        fullWidth
        variant="outlined"
        placeholder="Type your message..."
        value={input}
        onChange={(e) => { setInput(e.target.value) }}
      />
      <Button variant="contained" color="primary" onClick={handleSend} sx={{ marginLeft: 2 }}>
        Send
      </Button>
    </Box>
  )
}

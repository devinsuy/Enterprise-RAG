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

  const handleKeyPress = (e: { keyCode: number }) => {
    if (e.keyCode === 13) { // enter key was pressed
      handleSend()
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
        onKeyDown={handleKeyPress}
        required
      />
      <Button variant="contained" color="primary" onClick={handleSend} sx={{ marginLeft: 2 }}>
        Send
      </Button>
    </Box>
  )
}

import React, { useState } from 'react'
import './App.css'
import '@chatscope/chat-ui-kit-styles/dist/default/styles.min.css'
import { MainContainer, ChatContainer, MessageList, Message, MessageInput, MessageModel } from '@chatscope/chat-ui-kit-react'
import axios from 'axios'
import { ChatHistoryResponse, ChatMessage, LLMMessage } from './types'
import { API_ENDPOINTS } from './config'


const App: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [loading, setLoading] = useState(false)
  const [chatHistory, setChatHistory] = useState<LLMMessage[]>([])

  const getTimeStr = () => new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })

  const handleSendMessage = async (input: string) => {
    if (input.trim() === '') return

    const newMessage: ChatMessage = { user: 'User', text: input, timestamp: getTimeStr()}
    setMessages([...messages, newMessage])
    setLoading(true)

    try {
      const response: ChatHistoryResponse = await axios.post(API_ENDPOINTS.chat, {
        existing_chat_history: chatHistory,
        prompt: input
      })
      console.log(JSON.stringify(response))
      const { new_chat_history, llm_response_text} = response.data
      setChatHistory(new_chat_history) // Update chat history state for subsequent requests

      const llmMsg = { user: 'LLM', text: llm_response_text, timestamp: getTimeStr() }
      setMessages([...messages, llmMsg])
      console.log(JSON.stringify(messages))
      console.log(JSON.stringify(chatHistory))

    } catch (error) {
      console.error('Error sending message:', error)
    } finally {
      setLoading(false)
    }
  }

  const getMessageModel = (message: ChatMessage): MessageModel => {
    return {
      message: message.text,
      sentTime: message.timestamp,
      sender: message.user,
      direction: message.user === 'User' ? 'outgoing' : 'incoming',
      position: 'single'
    }
  }

  return (
    <div className="chat-container">
      <MainContainer>
        <ChatContainer>
          <MessageList>
            {messages.map((msg, index) => (
              <Message key={index} model={getMessageModel(msg)} />
            ))}
            {loading && <Message model={{ message: "Typing...", sentTime: "just now", sender: "Bot", direction: "incoming", position: "single" }} />}
          </MessageList>
          <MessageInput placeholder="Type your message..." onSend={handleSendMessage} attachButton={false} />
        </ChatContainer>
      </MainContainer>
    </div>
  )
}

export default App

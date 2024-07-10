import React, { createContext, useContext, useState, type ReactNode, type FC } from 'react'
import { type ChatHistoryResponse, type LLMMessage, type ChatMessage } from '../types'
import axios from 'axios'
import { API_ENDPOINTS } from 'config'

interface ChatTab {
  id: number
  messages: ChatMessage[]
}

interface ChatContextType {
  tabs: ChatTab[]
  activeTab: number
  sendMessage: (text: string) => void
  addTab: () => void
  switchTab: (id: number) => void
}

const ChatContext = createContext<ChatContextType | undefined>(undefined)

interface ChatProviderProps {
  children: ReactNode
}

const getTimeStr = () => new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })

export const ChatProvider: FC<ChatProviderProps> = ({ children }) => {
  const [tabs, setTabs] = useState<ChatTab[]>([{ id: 0, messages: [] }])
  const [chatHistory, setChatHistory] = useState<LLMMessage[]>([])
  const [activeTab, setActiveTab] = useState(0)

  const sendMessage = async (text: string) => {
    const newMessage: ChatMessage = { user: 'User', text, timestamp: getTimeStr() }
    setTabs(prevTabs =>
      prevTabs.map(tab =>
        tab.id === activeTab ? { ...tab, messages: [...tab.messages, newMessage] } : tab
      )
    )

    try {
      const response: ChatHistoryResponse = await axios.post(API_ENDPOINTS.chat, {
        existing_chat_history: chatHistory,
        prompt: text
      })
      console.log(JSON.stringify(response))
      const { new_chat_history: newChatHistory, llm_response_text: llmResponseText } = response.data
      setChatHistory(newChatHistory) // Update chat history state for subsequent requests

      const llmMsg = { user: 'LLM', text: llmResponseText, timestamp: getTimeStr() }
      setTabs(prevTabs =>
        prevTabs.map(tab =>
          tab.id === activeTab ? { ...tab, messages: [...tab.messages, llmMsg] } : tab
        )
      )
    } catch (error) {
      console.error('Error sending message:', error)
    } finally {
      // setLoading(false)
    }

    // Simulate API call
    // setTimeout(() => {
    //   const responseMessage: ChatMessage = { user: 'LLM', text: 'Response from LLM', timestamp: new Date().toLocaleTimeString() }
    //   setTabs(prevTabs =>
    //     prevTabs.map(tab =>
    //       tab.id === activeTab ? { ...tab, messages: [...tab.messages, responseMessage] } : tab
    //     )
    //   )
    // }, 1000)
  }

  const addTab = () => {
    setTabs(prevTabs => [...prevTabs, { id: prevTabs.length, messages: [] }])
  }

  const switchTab = (id: number) => {
    setActiveTab(id)
  }

  return (
    <ChatContext.Provider value={{ tabs, activeTab, sendMessage, addTab, switchTab }}>
      {children}
    </ChatContext.Provider>
  )
}

export const useChat = () => {
  const context = useContext(ChatContext)
  if (!context) {
    throw new Error('useChat must be used within a ChatProvider')
  }
  return context
}

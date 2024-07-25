import React, { createContext, useContext, useState, type ReactNode, type FC } from 'react'
import { type ChatHistoryResponse, type LLMMessage, type ChatMessage, type PromptFnCalls } from '../types'
import axios from 'axios'
import { API_ENDPOINTS, API_KEY } from 'config'

interface ChatTab {
  id: number
  messages: ChatMessage[]
  chatHistory: LLMMessage[]
  fnCalls: PromptFnCalls[]
}

interface ChatContextType {
  loading: boolean
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

const getTimeStr = () => new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })

const parseText = (text: string): string => {
  // Create a DOM parser
  const parser = new DOMParser()
  // Wrap the input text with a root element to ensure it's well-formed XML
  const doc = parser.parseFromString(`<root>${text}</root>`, 'text/xml')

  // Extract the content from the <result> tag, if it exists
  const resultElement = doc.querySelector('result')
  if (resultElement) {
    return resultElement.textContent ?? ''
  }

  // If no <result> tag, remove all other tags and return the main content
  return text.replace(/<[^>]*>[^<]*<\/[^>]*>/g, '').replace(/<[^>]*\/>/g, '')
}

export const ChatProvider: FC<ChatProviderProps> = ({ children }) => {
  const [tabs, setTabs] = useState<ChatTab[]>([{ id: 0, messages: [], chatHistory: [], fnCalls: [] }])
  const [activeTab, setActiveTab] = useState(0)
  const [loading, setLoading] = useState<boolean>(false)

  const sendMessage = async (text: string) => {
    const newMessage: ChatMessage = { user: 'User', text, timestamp: getTimeStr() }
    setTabs(prevTabs =>
      prevTabs.map(tab =>
        tab.id === activeTab ? { ...tab, messages: [...tab.messages, newMessage] } : tab
      )
    )

    setLoading(true)

    // Temporarily add a loading message
    const loadingMessage: ChatMessage = { user: 'LLM', text: 'Loading...', timestamp: '' }
    setTabs(prevTabs =>
      prevTabs.map(tab =>
        tab.id === activeTab ? { ...tab, messages: [...tab.messages, loadingMessage] } : tab
      )
    )

    try {
      const response: ChatHistoryResponse = await axios.post(
        API_ENDPOINTS.chat,
        {
          existing_chat_history: tabs[activeTab].chatHistory,
          prompt: text,
        },
        {
          headers: {
            Authorization: API_KEY,
          },
        }
      )

      console.log(JSON.stringify(response))
      const { new_chat_history: newChatHistory, llm_response_text: llmResponseText, fn_calls: fnCalls } = response.data
      const parsedResponseText = parseText(llmResponseText)
      const llmMsg = { user: 'LLM', text: parsedResponseText, timestamp: getTimeStr() }

      // Update the current tab with the new messages and chat history
      setTabs(prevTabs =>
        prevTabs.map(tab => {
          if (tab.id !== activeTab) return tab
          const messagesWithoutLoadingMsg = tab.messages.filter((msg) => msg.text !== 'Loading...')
          return {
            ...tab,
            messages: [...messagesWithoutLoadingMsg, llmMsg],
            fnCalls: [...tab.fnCalls, fnCalls],
            chatHistory: newChatHistory
          }
        })
      )
    } catch (error) {
      console.error('Error sending message:', error)
      const errorMessage: ChatMessage = { user: 'System', text: 'Error sending message. Please try again.', timestamp: getTimeStr() }
      setTabs(prevTabs =>
        prevTabs.map(tab =>
          tab.id === activeTab ? { ...tab, messages: [...tab.messages.filter((msg) => msg.text !== 'Loading...'), errorMessage] } : tab
        )
      )
    } finally {
      setLoading(false)
    }
  }

  const addTab = () => {
    setTabs(prevTabs => [...prevTabs, { id: prevTabs.length, messages: [], chatHistory: [], fnCalls: [] }])
  }

  const switchTab = (id: number) => {
    setActiveTab(id)
  }

  return (
    <ChatContext.Provider value={{ tabs, activeTab, sendMessage, addTab, switchTab, loading }}>
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

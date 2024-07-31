import React, { createContext, useContext, useState, type ReactNode, type FC } from 'react'
import { type ChatHistoryResponse, type LLMMessage, type ChatMessage, type PromptFnCalls } from '../types'
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
  tuners: string[] | null
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
  const parser = new DOMParser()
  const doc = parser.parseFromString(`<root>${text}</root>`, 'text/xml')
  const resultElement = doc.querySelector('result')
  if (resultElement) {
    return resultElement.textContent ?? ''
  }
  return text.replace(/<[^>]*>[^<]*<\/[^>]*>/g, '').replace(/<[^>]*\/>/g, '')
}

const fetchTuners = async (chatHistory: any, previousTuners: string[] | null): Promise<string[] | null> => {
  try {
    const response = await fetch(API_ENDPOINTS.tuners, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: API_KEY,
      },
      body: JSON.stringify({
        existing_chat_history: chatHistory,
        previous_tuners: previousTuners ?? [],
      }),
    })
    const data: ChatHistoryResponse = await response.json()
    const { llm_response_text: llmResponseText } = data.data
    console.log(`Generated dynamic tuners: ${llmResponseText}`)
    return llmResponseText.split(',').slice(0, 8)
  } catch (error) {
    console.error(`Failed to fetch dynamic tuners: ${error}`)
    return null
  }
}

export const ChatProvider: FC<ChatProviderProps> = ({ children }) => {
  const [tabs, setTabs] = useState<ChatTab[]>([{ id: 0, messages: [], chatHistory: [], fnCalls: [] }])
  const [activeTab, setActiveTab] = useState(0)
  const [loading, setLoading] = useState<boolean>(false)
  const [prevTuners, setPrevTuners] = useState<string[] | null>(null)
  const [tuners, setTuners] = useState<string[] | null>(null)

  const sendMessage = async (text: string) => {
    setPrevTuners(tuners)
    setTuners(null) // Reset tuners, null state to indicate loading

    const newMessage = { id: `msg-${Date.now()}`, user: 'User', text, timestamp: getTimeStr() }
    setTabs(prevTabs =>
      prevTabs.map(tab => (tab.id === activeTab ? { ...tab, messages: [...tab.messages, newMessage] } : tab))
    )

    setLoading(true)

    // Temporarily add a loading message
    const loadingMessageId = `loading-${Date.now()}`
    const loadingMessage = { id: loadingMessageId, user: 'LLM', text: '', timestamp: '' }
    setTabs(prevTabs =>
      prevTabs.map(tab => (tab.id === activeTab ? { ...tab, messages: [...tab.messages, loadingMessage] } : tab))
    )

    try {
      const response = await fetch(`${API_ENDPOINTS.chat}/stream?api_key=${API_KEY}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt: text, existing_chat_history: tabs[activeTab].chatHistory }),
      })

      if (!response.ok) {
        throw new Error('Network response was not ok')
      }
      if (!response.body) {
        throw new Error(`Got null response body: ${JSON.stringify(response)}`)
      }

      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''
      let accumulatedText = ''

      const processChunk = (chunk: any) => {
        const newAccumulatedText = accumulatedText + (chunk.text as string)
        accumulatedText = newAccumulatedText // update outer accumulatedText
        const timestamp = getTimeStr()

        setTabs(prevTabs =>
          prevTabs.map(tab => {
            if (tab.id !== activeTab) return tab
            const updatedMessages = tab.messages.map(msg => {
              if (msg.id === loadingMessageId) {
                return { ...msg, text: newAccumulatedText, timestamp }
              }
              return msg
            })
            return {
              ...tab,
              messages: updatedMessages,
            }
          })
        )
      }

      let newChatHistory: LLMMessage[] = []
      let fnCalls: PromptFnCalls[] = []

      while (true) {
        const { value, done } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        console.log(`CHUNK IS: ${JSON.stringify(buffer)}`)
        console.log('================================')
        const lines = buffer.split('\n')

        for (let i = 0; i < lines.length - 1; i++) {
          let line = lines[i].trim()
          if (line.startsWith('data: ')) {
            line = line.slice(6).trim()
            if (line === '[DONE]') {
              break
            }
            if (line) {
              try {
                const parsedData = JSON.parse(line)
                if (parsedData.error) {
                  throw new Error(parsedData.error)
                }
                const { delta } = parsedData
                if (delta?.text) {
                  processChunk(delta)
                }
                if (parsedData.new_chat_history) {
                  newChatHistory = parsedData.new_chat_history
                }
                if (parsedData.fn_calls) {
                  fnCalls = parsedData.fn_calls
                }
              } catch (e) {
                setLoading(false)
                console.error('Error parsing chunk:', e)
                const errorMessage = { id: `error-${Date.now()}`, user: 'System', text: 'An error occurred. Please try sending your message again.', timestamp: getTimeStr() }
                setTabs(prevTabs =>
                  prevTabs.map(tab =>
                    tab.id === activeTab ? { ...tab, messages: [...tab.messages.filter((msg) => msg.id !== loadingMessageId), errorMessage] } : tab
                  )
                )
                return // Exit the function after handling the error
              }
            }
          }
        }
        buffer = lines[lines.length - 1] // Keep the last line if it's partial
      }
      // Fetch tuners once the full message is received
      const newTuners = await fetchTuners(newChatHistory, prevTuners)
      setPrevTuners(tuners)
      setTuners(newTuners)
    } catch (error) {
      setTuners(prevTuners) // Restore tuners
      setPrevTuners(null)
      console.error('Error sending message:', error)
      const errorMessage = { id: `error-${Date.now()}`, user: 'System', text: 'An error occurred. Please try sending your message again.', timestamp: getTimeStr() }
      setTabs(prevTabs =>
        prevTabs.map(tab =>
          tab.id === activeTab ? { ...tab, messages: [...tab.messages.filter((msg) => msg.id !== loadingMessageId), errorMessage] } : tab
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
    <ChatContext.Provider value={{ tabs, activeTab, sendMessage, addTab, switchTab, loading, tuners }}>
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

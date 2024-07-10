import { useState } from 'react'
import { type ChatMessage } from 'types'

interface ChatTab {
  id: number
  messages: ChatMessage[]
}

export const useChat = () => {
  const [tabs, setTabs] = useState<ChatTab[]>([{ id: 0, messages: [] }])
  const [activeTab, setActiveTab] = useState(0)

  const sendMessage = (text: string) => {
    const newMessage: ChatMessage = { user: 'User', text, timestamp: new Date().toLocaleTimeString() }
    setTabs(tabs.map(tab =>
      tab.id === activeTab ? { ...tab, messages: [...tab.messages, newMessage] } : tab
    ))
    // Simulate API call
    setTimeout(() => {
      const responseMessage: ChatMessage = { user: 'LLM', text: 'Response from LLM', timestamp: new Date().toLocaleTimeString() }
      setTabs(tabs =>
        tabs.map(tab =>
          tab.id === activeTab ? { ...tab, messages: [...tab.messages, responseMessage] } : tab
        )
      )
    }, 1000)
  }

  const addTab = () => {
    setTabs([...tabs, { id: tabs.length, messages: [] }])
  }

  const switchTab = (id: number) => {
    setActiveTab(id)
  }

  return { tabs, activeTab, sendMessage, addTab, switchTab }
}

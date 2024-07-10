import React from 'react'
import { List, ListItem, ListItemText, styled } from '@mui/material'
import { useChat } from '../hooks/useChat'

// const ChatBubble = styled(ListItemText)(({ theme }) => ({
//   backgroundColor: '#e0f7fa', // Light cyan background
//   borderRadius: '15px', // Rounded corners
//   padding: '5px 15px', // Padding for the text
//   //   margin: '10px 0', // Margin for spacing between bubbles
//   maxWidth: '30%', // Maximum width of the bubble
//   wordWrap: 'break-word', // Ensure long words break to the next line
//   alignSelf: 'flex-start', // Align bubbles to the start (left)
//   // Optional: Add a shadow for a more elevated look
//   boxShadow: '0px 1px 5px rgba(0, 0, 0, 0.1)',
// }))

// interface ChatListItemProps {
//   primary: string
//   secondary?: string
//   className?: string
// }

// const ChatListItem = ({ primary, secondary, className }: ChatListItemProps) => (
//     <ListItem>
//         <ChatBubble primary={primary} secondary={secondary} className={className}/>
//     </ListItem>
// )

export const MessageList: React.FC = () => {
  const { tabs, activeTab } = useChat()

  return (
    <List sx={{ flexGrow: 1, overflowY: 'auto' }}>
      {tabs[activeTab].messages.map((msg, i) => (
        <ListItem key={i} alignItems="flex-start" className={msg.user === 'LLM' ? 'llm-message-container' : 'user-message-container'}>
          <ListItemText primary={msg.text} secondary={msg.timestamp} className={msg.user === 'LLM' ? 'llm-message' : 'user-message'}/>
        </ListItem>
      ))}
    </List>
  )
}

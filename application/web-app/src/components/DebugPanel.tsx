import React, { useState } from 'react'
import { Drawer, Typography, IconButton, Button } from '@mui/material'
import CloseIcon from '@mui/icons-material/Close'
import { useChat } from 'hooks/useChat'
import { type ToolUseContent } from 'types'

interface DebugPanelProps {
  open: boolean
  onClose: () => void
}

type DebugView = 'History' | 'ToolCalls'

export const DebugPanel = ({ open, onClose }: DebugPanelProps) => {
  const { tabs, activeTab } = useChat()
  const [selectedView, setSelectedView] = useState<DebugView>('History')

  return (
      <Drawer anchor="right" open={open} onClose={onClose}>
        <div style={{ width: '700px', padding: 16 }}>
          <IconButton onClick={onClose}>
            <CloseIcon />
          </IconButton>
          <Typography variant="h6">Debug Panel</Typography>

          <div style={{ marginTop: '20px' }}>
            <Typography variant="body1" sx={{ marginBottom: '10px' }}>Selected View</Typography>

            <Button onClick={() => { setSelectedView('History') }} variant={selectedView === 'History' ? 'contained' : 'outlined'} sx={{ marginRight: '20px' }}>Msg History</Button>
            <Button onClick={() => { setSelectedView('ToolCalls') }} variant={selectedView === 'ToolCalls' ? 'contained' : 'outlined'}>FN Calls</Button>
          </div>

          {selectedView === 'History' && tabs[activeTab].chatHistory.map((message, i) => {
            return message.content.map((msgContent) => {
              if (msgContent.type === 'tool_use' || msgContent.type === 'tool_result') {
                return undefined
              }
              return <Typography key={i} sx={{ paddingBottom: '30px' }} variant="body1" className={message.role === 'assistant' ? 'llm-message' : 'user-message'}>{JSON.stringify(message.content, null, 2)}</Typography>
            })
          })}

          {selectedView === 'ToolCalls' && tabs[activeTab].fnCalls.map((promptFnCalls, i) => {
            return (<>
              <Typography key={i} variant='body1'>{promptFnCalls.user_prompt}</Typography>
              {promptFnCalls.fn_calls.map((fnMsg, j) => {
                if (fnMsg.type !== 'tool_use') {
                  return undefined
                }
                return <Typography key={`${i}-${j}`} variant="body1">{JSON.stringify((fnMsg as ToolUseContent).input)}</Typography>
              })}
            </>)
          })}
        </div>
      </Drawer>
  )
}

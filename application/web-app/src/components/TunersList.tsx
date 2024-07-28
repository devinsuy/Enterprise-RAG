import { Box, Button, Grow } from '@mui/material'
import { useChat } from 'hooks/useChat'
import { useEffect, useState } from 'react'

export const TunersList: React.FC = () => {
  const { sendMessage, tuners } = useChat()
  const [showTuners, setShowTuners] = useState(false)

  useEffect(() => {
    if (tuners && tuners.length > 0) {
      setShowTuners(true)
    } else {
      setShowTuners(false)
    }
  }, [tuners])

  if (!showTuners) {
    return <></>
  }

  return (
    <Grow in={showTuners}>
        <Box sx={{ display: 'flex', justifyContent: 'center', p: 1, borderTop: '1px solid #ccc' }}>
          {tuners?.map((tuner, i) => (
            <Button
              key={`${tuner}-${i}`}
              variant="contained"
              sx={{
                mx: 0.5,
                textTransform: 'none',
              }}
              onClick={() => {
                sendMessage(tuner)
              }}
            >
              {tuner}
            </Button>
          ))}
        </Box>
      </Grow>
  )
}

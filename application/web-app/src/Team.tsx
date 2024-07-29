import React from 'react'
import { Box, Typography, Grid, Avatar, Link } from '@mui/material'

const teamMembers = [
  { name: 'Robert Greer', email: 'robert.greer@berkeley.edu', img: require('./assets/Robert.jpg') },
  { name: 'Thomas Lai', email: 'thomaslai.com@berkeley.edu', img: require('./assets/Thomas.jpg') },
  { name: 'Randy Louie', email: 'rlouie@berkeley.edu', img: require('./assets/Randy.png') },
  { name: 'Devin Suy', email: 'devinsuy@berkeley.edu', img: require('./assets/Devin.jpg') },
  { name: 'Nadia Tantsyura', email: 'nadia.tantsyura@berkeley.edu', img: require('./assets/Nadia.png') },
]

export const Team: React.FC = () => {
  return (
    <Box
      sx={{
        padding: '40px',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        maxWidth: '90%',
        margin: '0 auto',
        textAlign: 'center',
      }}
    >
      <Typography variant="h5" component="h2" gutterBottom sx={{ paddingBottom: '5px' }}>
        <strong>Our Team</strong>
      </Typography>
      <Typography variant="body1" paragraph sx={{ paddingBottom: '15px', maxWidth: '45%', textAlign: 'center' }}>
        Scraps2Scrumptious is the capstone project of a passionate team of data science master&rsquo;s students from UC Berkeley&apos;s MIDS program during the Summer 2024 semester. Our project embodies our dedication to merging technology and a passion for food to create a tool that enhances everyday cooking experiences.
      </Typography>
      <Grid container sx={{ paddingTop: '2%' }} spacing={4} justifyContent="center">
        {teamMembers.map((member, index) => (
          <Grid item key={index}>
            <Avatar
              alt={member.name}
              src={member.img}
              sx={{ width: 150, height: 150, margin: '0 auto' }}
            />
            <Typography variant="body1" component="div" sx={{ fontWeight: 'bold', marginTop: '10px' }}>
              {member.name}
            </Typography>
            <Typography variant="body2" component="div">
              <Link href={`mailto:${member.email}`} sx={{ color: 'inherit', textDecoration: 'none' }}>
                {member.email}
              </Link>
            </Typography>
          </Grid>
        ))}
      </Grid>
    </Box>
  )
}

export default Team

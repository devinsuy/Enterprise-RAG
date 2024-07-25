import React from 'react'
import { Box, Typography } from '@mui/material'

export const About: React.FC = () => {
  return (
    <Box
      sx={{
        padding: '40px',
        height: '100vh',
        justifyContent: 'center',
        maxWidth: '90%'
      }}
    >
      <Typography variant="h5" component="h2" gutterBottom sx={{ paddingBottom: '5px' }}>
        <strong>About Us</strong>
      </Typography>
      <Typography variant="body1" paragraph sx={{ paddingBottom: '15px' }}>
        Welcome to Scraps2Scrumptious, a web application that tailor makes culinary recipes to one&rsquo;s unique palette and kitchen! Whether you&rsquo;re a professional chef, a home cook, or someone who hasn&rsquo;t gone to the grocery store in a while, Scraps2Scrumptious is here to inspire and guide you to making a delicious dish.
      </Typography>

      <Typography variant="h5" component="h2" gutterBottom sx={{ paddingBottom: '5px' }}>
        <strong>Our Mission</strong>
      </Typography>
      <Typography variant="body1" paragraph sx={{ paddingBottom: '15px' }}>
        At Scraps2Scrumptious, we believe that everyone should have the opportunity to enjoy delicious, homemade meals without the stress of scrolling through dozens of recipes online. Our mission is to simplify the cooking experience by leveraging the power of AI to generate personalized recipes that cater to your unique tastes and dietary needs.
      </Typography>

      <Typography variant="h5" component="h2" gutterBottom sx={{ paddingBottom: '5px' }}>
        <strong>How it works</strong>
      </Typography>
      <Typography variant="body1" paragraph sx={{ paddingBottom: '15px' }}>
        Scraps2Scrumptious utilizes state-of-the-art Retrieval-Augmented Generation (RAG) technology to craft custom recipes based on your specific queries. Whether you&apos;re searching for a vegetarian dish, a low-carb meal, or an Asian fusion recipe, our AI-powered platform retrieves and combines the best elements from a vast database of 500,000+ recipes to create a unique culinary experience just for you.
      </Typography>

      <Typography variant="h5" component="h2" gutterBottom sx={{ paddingBottom: '5px' }}>
        <strong>How to use Scraps2Scrumptious</strong>
      </Typography>
      <Typography variant="body1" paragraph sx={{ paddingBottom: '15px' }}>
        1. <strong>Input Your Query:</strong> Start by entering your preferences, ingredients, or any specific dish you have in mind.
      </Typography>
      <Typography variant="body1" paragraph sx={{ paddingBottom: '15px' }}>
        2. <strong>AI Generation:</strong> Our advanced RAG system goes to work, retrieving relevant information from a comprehensive recipe database and generating a customized recipe tailored to your input.
      </Typography>
      <Typography variant="body1" paragraph sx={{ paddingBottom: '15px' }}>
        3. <strong>Fine Tuning:</strong> Don&rsquo;t like tomatoes in your sandwich? Don&rsquo;t have cumin at home? Just enter that in the chat box or tell our algorithm what you&rsquo;re thinking! It will generate a new recipe that will remove that ingredient or even substitute it.
      </Typography>
      <Typography variant="body1" paragraph sx={{ paddingBottom: '15px' }}>
        4. <strong>Enjoy Cooking:</strong> Follow the step-by-step instructions provided by Scraps2Scrumptious and enjoy a delightful meal designed to suit your tastes and dietary preferences.
      </Typography>
    </Box>
  )
}

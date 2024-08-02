import React from 'react'
import { Box, Typography, Container, Card, CardContent, Grid, Link } from '@mui/material'

const surveyLinkUrl = 'https://berkeley.qualtrics.com/jfe/form/SV_8CzqCn6sJ8kCyPQ'

export const About: React.FC = () => {
  return (
    <Container maxWidth="lg" sx={{ paddingTop: '40px', paddingBottom: '40px' }}>
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          textAlign: 'center',
          marginBottom: '40px',
        }}
      >
        <Typography variant="h4" component="h1" gutterBottom>
          <strong>About Us</strong>
        </Typography>
        <Typography variant="body1" paragraph sx={{ maxWidth: '90%' }}>
          Welcome to Scraps2Scrumptious, your personalized culinary assistant. Our platform transforms your available ingredients into delectable, tailored recipes, reducing food waste and enhancing your cooking experience. Whether you are a seasoned chef, a home cook, or someone with limited groceries, Scraps2Scrumptious is designed to inspire and guide you in creating mouthwatering dishes.
        </Typography>
      </Box>

      <Grid container spacing={4}>
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h5" component="h2" gutterBottom>
                <strong>Our Mission</strong>
              </Typography>
              <Typography variant="body1" paragraph>
                At Scraps2Scrumptious, our mission is to make delicious, homemade meals accessible to everyone without the hassle of browsing endless recipes online. By harnessing the power of AI, we generate personalized recipes that meet your unique tastes and dietary requirements, making the cooking process simpler and more enjoyable.
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h5" component="h2" gutterBottom>
                <strong>How It Works</strong>
              </Typography>
              <Typography variant="body1" paragraph>
                Scraps2Scrumptious uses advanced Retrieval-Augmented Generation (RAG) technology to create customized recipes based on your input. Whether you&apos;re looking for a vegetarian meal, a low-carb option, or a fusion dish, our AI-driven platform searches through a vast database of over 500,000 recipes to deliver a unique culinary experience tailored just for you.
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h5" component="h2" gutterBottom>
                <strong>How to Use Scraps2Scrumptious</strong>
              </Typography>
              <Typography variant="body1" paragraph>
                1. <strong>Start Chatting:</strong> Share your preferences, ingredients, or any specific dish you have in mind with our AI.
              </Typography>
              <Typography variant="body1" paragraph>
                2. <strong>AI Generation:</strong> Our RAG system gets to work, retrieving relevant recipes from our extensive database and generating a personalized recipe just for you.
              </Typography>
              <Typography variant="body1" paragraph>
                3. <strong>Customize Further:</strong> If you dislike certain ingredients or are missing some, simply let our AI know. It will adjust the recipe by removing or substituting those ingredients.
              </Typography>
              <Typography variant="body1" paragraph>
                4. <strong>Click Dynamic Tuners:</strong> Easily refine your recipes further by clicking on dynamic tuners that appear during your chat, offering you suggestions to fine-tune the recipe based on your evolving needs and preferences.
              </Typography>
              <Typography variant="body1" paragraph>
                5. <strong>Enjoy Cooking:</strong> Follow the step-by-step instructions provided by Scraps2Scrumptious and savor a meal perfectly suited to your tastes and dietary needs.
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="body1" paragraph>
                Discover the future of personalized cooking with Scraps2Scrumptious. Your feedback is invaluable to us, so please take a moment to complete <Link href={surveyLinkUrl} target="_blank" rel="noopener noreferrer" sx={{ color: '#0000EE' }}>our survey</Link> after trying the app. Enjoy your culinary journey with us!
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Container>
  )
}

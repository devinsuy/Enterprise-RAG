import React from 'react'
import { Box, Typography, Container, Card, CardContent, Grid, Link } from '@mui/material'

export const Technology: React.FC = () => {
  const surveyLinkUrl = 'https://berkeley.qualtrics.com/jfe/form/SV_8CzqCn6sJ8kCyPQ'

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
          <strong>Technology</strong>
        </Typography>
        <Typography variant="body1" paragraph sx={{ maxWidth: '80%' }}>
          At Scraps2Scrumptious, we leverage cutting-edge technology to bring you personalized, delicious recipes tailored to your unique tastes and available ingredients. Here&rsquo;s an overview of the technology that powers our platform.
        </Typography>
      </Box>

      <Grid container spacing={4}>
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h5" component="h2" gutterBottom>
                <strong>Flow Diagram</strong>
              </Typography>
              <Box sx={{ display: 'flex', justifyContent: 'center' }}>
                <img src={require('./assets/sys_architecture.png')} alt="Flow Diagram" style={{ maxWidth: '100%' }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h5" component="h2" gutterBottom>
                <strong>Advanced Retrieval Chain</strong>
              </Typography>
              <Typography variant="body1" paragraph>
                Our advanced retrieval chain ensures that the recipes we provide are highly relevant and diverse, avoiding redundancy or overly similar content.
              </Typography>
              <Typography variant="body1" paragraph>
                <strong>MMR Coarse Search:</strong> Maximum Marginal Relevance (MMR) helps us find the most relevant recipes for your query while providing a diverse set of options.
              </Typography>
              <Typography variant="body1" paragraph>
                <strong>Self-query LLM Validation:</strong> Our Language Model (LLM) ensures that the retrieved recipes adhere to your dietary restrictions, preferences, allergies, and other considerations.
              </Typography>
              <Typography variant="body1" paragraph>
                <strong>Reranker:</strong> This component sifts through the top recipes to provide the best match for your query, ensuring the final suggestion is the most suitable one based on your requirements.
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h5" component="h2" gutterBottom>
                <strong>LLM Orchestrator</strong>
              </Typography>
              <Typography variant="body1" paragraph>
                Our system employs an advanced LLM orchestrator that manages the various components involved in recipe generation and refinement.
              </Typography>
              <Typography variant="body1" paragraph>
                <strong>Agent Functional Calls:</strong> Our model autonomously determines when to query the recipe vector database and when to perform Google searches, ensuring accurate and comprehensive recipe details.
              </Typography>
              <Typography variant="body1" paragraph>
                <strong>Prompt Augmentation:</strong> The prompts are dynamically augmented based on your ongoing conversation, allowing for continuous refinement of the recipes to better match your dietary needs and tastes.
              </Typography>
              <Typography variant="body1" paragraph>
                <strong>Web Search:</strong> When necessary, our system performs web searches to retrieve the most up-to-date and comprehensive information about specific ingredients or cooking techniques.
              </Typography>
              <Typography variant="body1" paragraph>
                <strong>Validation:</strong> This component checks the generation results from the agents to ensure that the final recipe meets all your specified requirements and dietary restrictions.
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h5" component="h2" gutterBottom>
                <strong>Context-Aware Dynamic Prompting</strong>
              </Typography>
              <Typography variant="body1" paragraph>
                Our app features context-aware dynamic prompting that allows you to continuously refine your recipe requirements.
              </Typography>
              <Typography variant="body1" paragraph>
                <strong>Context-Aware Tuners:</strong> These tuners appear at the bottom of the chat and suggest options based on your chat history and current recipe requirements, making it easy to customize the dish to your liking.
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h5" component="h2" gutterBottom>
                <strong>Key Innovations</strong>
              </Typography>
              <Typography variant="body1" paragraph>
                1. <strong>Advanced Retrieval System:</strong> Using the Qdrant vector store, our system efficiently sifts through over 500,000 recipes to deliver highly relevant suggestions.
              </Typography>
              <Typography variant="body1" paragraph>
                2. <strong>Dynamic Querying with Agents:</strong> Our model autonomously determines when to query the recipe vector database and when to perform Google searches, ensuring accurate and comprehensive recipe details.
              </Typography>
              <Typography variant="body1" paragraph>
                3. <strong>LLM Gatekeeper:</strong> Our language model acts as a gatekeeper, ranking and evaluating recipes to ensure they meet your specified requirements and dietary restrictions.
              </Typography>
              <Typography variant="body1" paragraph>
                4. <strong>Context-Aware Dynamic Prompt Tuners:</strong> These tuners allow you to continuously refine recipes to match your dietary needs, personal tastes, or available ingredients. Easily request ingredient substitutes to make the most of what you have at home.
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Container>
  )
}

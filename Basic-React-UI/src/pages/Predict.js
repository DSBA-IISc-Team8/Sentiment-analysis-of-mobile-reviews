import React, { useState } from 'react';
import axios from 'axios';
import {
  Flex,
  Box,
  Heading,
  FormControl,
  FormLabel,
  Button,
  CircularProgress,
  Textarea,
  Stack,
  Image,
  ListItem,
  VStack,
  SimpleGrid,
  Container,
  OrderedList,
  UnorderedList,
  Text,
} from '@chakra-ui/react';
import { ViewIcon } from '@chakra-ui/icons';

import ErrorMessage from '../components/ErrorMessage';
import positive from '../images/positive.png';
import neutral from '../images/neutral.png';
import negative from '../images/negative.png';
import legend from '../images/sentiment.png';

export default function Predict() {
  const [text, setText] = useState('');
  const [error, setError] = useState('');
  const [res, setRes] = useState('');
  const [sentiment, setSentiment] = useState('');
  const [feature_sentiment, setFeatureSentiment] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = event => {
    event.preventDefault();

    setIsLoading(true);

    try {
      axios.post(`http://localhost:8000/predict`, { text }).then(res => {
        console.log(res.data);
        setRes(res.data);

        const res_sentiment = res.data.sentiment.trim().toLowerCase();
        if (res_sentiment === 'positive') setSentiment(positive);
        else if (res_sentiment === 'negative') setSentiment(negative);
        else setSentiment(neutral);

        const res_feature_sentiment = res.data.feature_sentiment;
        setFeatureSentiment(res_feature_sentiment);

        setIsLoading(false);
      });
    } catch (error) {
      setError('Unknown Error');
      setIsLoading(false);
    }
  };

  return (
    <Flex width="full" align="center" justifyContent="center">
      <Box
        p={8}
        maxWidth="1000px"
        minWidth="800px"
        borderWidth={1}
        borderRadius={8}
        boxShadow="lg"
      >
        <Box textAlign="center">
          <Heading>Find the Sentiment</Heading>
        </Box>
        <Box my={4} textAlign="center">
          <form onSubmit={handleSubmit}>
            {error && <ErrorMessage message={error} />}
            <FormControl isRequired>
              <FormLabel htmlFor="text">Text</FormLabel>
              <Textarea
                id="text"
                placeholder="Enter text to predict the sentiment"
                size="sm"
                resize="both"
                onChange={event => setText(event.currentTarget.value)}
              />
            </FormControl>
            <Button
              type="submit"
              colorScheme="teal"
              variant="solid"
              mt={4}
              leftIcon={<ViewIcon />}
            >
              {isLoading ? (
                <CircularProgress isIndeterminate size="24px" />
              ) : (
                'Predict'
              )}
            </Button>
          </form>
          {res && (
            <>
              <SimpleGrid columns={2} spacing={10} mt={2}>
                <Box p={5}>
                  <VStack spacing={4} align="center">
                    <Heading fontSize="xl">Overall Sentiment</Heading>
                    <Image src={sentiment} boxSize="67px" />
                  </VStack>
                </Box>
                <Box p={5}>
                  <VStack spacing={4} align="center">
                    <Heading fontSize="xl">Feature Sentiment</Heading>
                    <Box>
                      <OrderedList>
                        {Object.entries(feature_sentiment).map(
                          ([key, value]) => {
                            value = value[0].trim().toLowerCase();
                            var fea_sentiment;
                            if (value === 'positive') fea_sentiment = positive;
                            else if (value === 'negative')
                              fea_sentiment = negative;
                            else fea_sentiment = neutral;

                            return (
                              <ListItem key={key} mb={5}>
                                <Flex>
                                  <Text mr={3}>{key} </Text>
                                  <Image src={fea_sentiment} boxSize="30px" />
                                </Flex>
                              </ListItem>
                            );
                          }
                        )}
                      </OrderedList>
                    </Box>
                  </VStack>
                </Box>
                <Box></Box>
              </SimpleGrid>
              <Box colSpan={2} align="right">
                <img src={legend} style={{ height: '150px' }} />
              </Box>
            </>
          )}
        </Box>
      </Box>
    </Flex>
  );
}

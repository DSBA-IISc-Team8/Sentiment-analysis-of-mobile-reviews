import React from 'react';
import {
  ChakraProvider,
  Box,
  Textarea,
  VStack,
  Grid,
  theme,
  Img,
  FormLabel,
  Flex,
  Spacer,
} from '@chakra-ui/react';
import { ColorModeSwitcher } from './ColorModeSwitcher';
import Predict from './pages/Predict';
import logo from './images/IISC.png';

function App() {
  return (
    <ChakraProvider theme={theme}>
      <Box textAlign="center" fontSize="xl">
        <Grid p={3}>
          <Flex>
            <Img src={logo} boxSize="100px" objectFit="cover" />
            <Spacer />
            <ColorModeSwitcher justifySelf="flex-end" />
          </Flex>
          <Predict />
        </Grid>
      </Box>
    </ChakraProvider>
  );
}

export default App;

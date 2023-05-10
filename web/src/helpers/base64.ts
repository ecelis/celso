/**
   Copyright 2023 Ernesto A. Celis de la Fuente

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/
function decodeBase64Image(dataString: string) {
    const matches = dataString.match(/^data:([A-Za-z-+\/]+);base64,(.+)$/),
    response = {
        type: null,
        data: null,
    };
  
    // @ts-ignore
    if (matches.length !== 3) {
      return new Error('Invalid input string');
    }
  
    // @ts-ignore
    response.type = matches[1];
    
    // @ts-ignore
    response.data = new Buffer(matches[2], 'base64');
  
    return response.data;
}

export default decodeBase64Image;
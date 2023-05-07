
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
import Link from "@mui/material/Link";
import Typography from "@mui/material/Typography";

function Footer() {
    return (
      <Typography variant="body2" color="text.secondary">
        {'Copyright © '}
        <Link color="inherit" href="https://celisdelafuente.net/">
          Ernesto Celis
        </Link>{' '}
        {new Date().getFullYear()}
        {'.'}
      </Typography>
    );
  }
  
  export default Footer;
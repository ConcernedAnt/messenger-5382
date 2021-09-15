import React from "react";
import { Box, Typography } from "@material-ui/core";

import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => ({
  root: {
    marginRight: 20,
    borderRadius: 10,
    backgroundColor: theme.palette.primary.main,
  },
  text: {
    fontSize: 10,
    color: theme.palette.otherUserText.main,
    letterSpacing: -0.5,
    padding: theme.spacing(0.5, 1),
  },
}));

// Renders the number of unread messages in the sidebar
const UnreadCounter = (props) => {
  const classes = useStyles();
  const { numUnread } = props;

  return (
    <Box className={classes.root}>
      <Typography className={classes.text}>{numUnread}</Typography>
    </Box>
  );
};

export default UnreadCounter;

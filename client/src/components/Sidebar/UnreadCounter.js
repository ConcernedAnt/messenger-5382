import React from "react";
import { Box, Typography } from "@material-ui/core";

import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles(() => ({
  root: {
    marginRight: 20,
    borderRadius: 10,
    backgroundColor: "#3F92FF",
  },
  text: {
    fontSize: 10,
    color: "#FFFFFF",
    letterSpacing: -0.5,
    padding: "3px 7px",
    fontWeight: "bold",
  },
}));

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

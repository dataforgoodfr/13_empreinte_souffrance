/* eslint-env node */
const formatCommand = "prettier . --check";

const lintStagedConfig = {
  "*": formatCommand,
};

export default lintStagedConfig;

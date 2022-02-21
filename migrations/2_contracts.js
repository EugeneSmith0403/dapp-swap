const token = artifacts.require("MyToken");


module.exports = function (deployer) {
  deployer.deploy(token, "SC", "SC", 1000, 1);
  // deployer.deploy(swap);
};

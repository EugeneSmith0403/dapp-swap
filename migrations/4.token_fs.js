const token = artifacts.require("MyToken");


module.exports = function (deployer) {
  deployer.deploy(token, "FS", "FS", 1000, 1);
};

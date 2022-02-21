const swap = artifacts.require("SwapVendor");

module.exports = function(deployer) {
    deployer.deploy(swap);
}

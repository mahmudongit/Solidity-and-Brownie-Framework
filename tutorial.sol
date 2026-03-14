// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract Tutorial{
     
      uint256 favoriteNumber;
       bool favoriteBool;


       struct People {
        uint256 favoriteNumber;
        string name;
       }

       People[] public people; //fixed you'll add number in btw the bracket: Dynamic array
       mapping(string => uint256) public nameToFavoriteNumber;

      function store (uint256 _favoriteNumber) public returns(uint256) { 
       favoriteNumber = _favoriteNumber;
         return favoriteNumber;
      }

 function retrieve () public view returns(uint256) {
    return favoriteNumber;
 }
  
 function addperson (string memory _name, uint256 _favoriteNumber) public {
    people.push(People({favoriteNumber: _favoriteNumber, name: _name}));
    nameToFavoriteNumber[_name] = _favoriteNumber;
 }

 function getAllPeople() public view returns (People[] memory) {
    return people;
}

 }
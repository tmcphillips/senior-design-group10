//
//  Player.swift
//  PA2
//
//  Created by Carl Lundin on 9/13/18.
//  Copyright © 2018 Lundin, Carl Erik Martin. All rights reserved.
//

import Foundation

class Player : CustomStringConvertible {
    var description: String {
        return "Your stats are: Total Shots \(totalShots), Total Hits: \(totalHits), Total Misses: \(totalMisses), Hits to Miss Ratio \(hitsToMissRatio)"
    }
    
    // player is a class so we can alter the game board and ships
    var battleShipBoard:BattleShipBoard = BattleShipBoard(human: false)
    var ships:[Ship] = []
    var human:Bool = false
    var totalHits:Int {
        didSet {
            totalShots += 1
        }
    }
    var totalMisses:Int {
        didSet {
            totalShots += 1
        }
    }
    var totalShots:Int {
        didSet {
            totalShots += 1
        }
    }
    
    var hitsToMissRatio:Double {
        return  totalMisses == 0 ? 0 : Double(totalHits / totalMisses)
    }
    
    init(human:Bool) {
        totalHits = 0
        totalMisses = 0
        totalShots = 0
        self.human = human
        self.battleShipBoard = BattleShipBoard( human:human)
        ships = [Ship(name: "Carrier",    length: 5, occupiedCells:[], symbol: Symbol.carrier,    hits: 0),
                 Ship(name: "Battleship", length: 4, occupiedCells:[], symbol: Symbol.battleship, hits: 0),
                 Ship(name: "Cruiser",    length: 3, occupiedCells:[], symbol: Symbol.cruiser,    hits: 0),
                 Ship(name: "Submarine",  length: 3, occupiedCells:[], symbol: Symbol.submarine,  hits: 0),
                 Ship(name: "Destroyer",  length: 2, occupiedCells:[], symbol: Symbol.destroyer,  hits: 0)]
    }
    func hasShips() -> Bool {
        for ship in ships {
            if ship.isSunk() == false {
                return true
            }
        }
        return false
    }
    
    func shoot(coord: Coordinate) {
        if battleShipBoard.grid[coord.row][coord.col].occupied {
            self.totalHits += 1
            battleShipBoard.grid[coord.row][coord.col].symbol = Symbol.hit
        }
        else {
            self.totalMisses += 1
            battleShipBoard.grid[coord.row][coord.col].symbol = Symbol.miss
        }
    }
}

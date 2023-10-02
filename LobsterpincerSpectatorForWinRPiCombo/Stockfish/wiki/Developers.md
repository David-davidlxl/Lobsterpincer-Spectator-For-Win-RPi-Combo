# Using Stockfish in your own project

## Resources

* [Advanced topics](Advanced-topics)
* [Commands](Commands)
* [Useful data](Useful-data)

## Terms of use

Stockfish is free and distributed under the [**GNU General Public License version 3**](https://github.com/official-stockfish/Stockfish/blob/master/Copying.txt) (GPL v3). Essentially, this means you are **free to do almost exactly what you want** with the program, including **distributing it** among your friends, **making it available for download** from your website, **selling it** (either by itself or as part of some bigger software package), or **using it as the starting point** for a software project of your own. This also means that you can distribute Stockfish [alongside your proprietary system](https://www.gnu.org/licenses/gpl-faq.html#GPLInProprietarySystem), but to do this validly, you must make sure that Stockfish and your program communicate at arm's length, that they are not combined in a way that would make them effectively a single program.

The only real limitation is that whenever you distribute Stockfish in some way, **you MUST always include the license and the full source code** (or a pointer to where the source code can be found) to generate the exact binary you are distributing. If you make any changes to the source code, these changes must also be made available under GPL v3.

# Participating in the project

Stockfish's improvement over the last decade has been a great community effort. There are a few ways to help contribute to its growth.

## Donating hardware

Improving Stockfish requires a massive amount of testing. You can donate your hardware resources by installing the [Fishtest Worker](https://github.com/glinscott/fishtest/wiki/Running-the-worker) and view the current tests on [Fishtest](https://tests.stockfishchess.org/tests).

## Improving the code

If you want to help improve the code, there are several valuable resources:

### Chessprogramming wiki

https://www.chessprogramming.org/

The wiki has many techniques used in Stockfish are explained with a lot of background information.  

[The section on Stockfish](https://www.chessprogramming.org/Stockfish) describes many features and techniques used by Stockfish. However, it is generic rather than being focused on Stockfish's precise implementation. Nevertheless, a helpful resource.

### Fishtest

New commits to stockfish can mostly be categorised in 2 categories:
#### Non functional changes

Changes that don't change the search behaviour, for example:
* Code cleanups
* Comments
* New commands

#### Functional changes

These change the search behaviour and lead to a different search tree.  
Every functional patch (commit) has to be verified by [Fishtest](https://tests.stockfishchess.org/tests), our testing framework.

Follow the steps described in our [Fishtest wiki](https://github.com/glinscott/fishtest/wiki/Creating-my-first-test), to create your first test.

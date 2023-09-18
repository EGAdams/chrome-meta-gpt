void Mode1Score::mode1P1Games() {
    _gameState->setServeSwitch( _gameState->getServeSwitch() + 1 );
    if ( _player1->getGames() >= GAMES_TO_WIN_SET ) {
        if ( _player1->getGames() == GAMES_TO_WIN_SET && _player2->getGames() == GAMES_TO_WIN_SET ) {
            _gameState->setTieBreak( 1 );
            _mode1TieBreaker.tieBreakEnable(); }
        if ( _gameState->getTieBreak() == 0 ) {
            if (( _player1->getGames() - _player2->getGames()) > 1 ) {
                _player1->setSets( _gameState, _player1->getSets() + 1 );
                _setLeds.updateSets();
                if ( _player1->getSets() == _player2->getSets()) {
                    _mode1WinSequences.p1TBSetWinSequence();
                    _gameState->setSetTieBreak( 1 );
                    _mode1TieBreaker.setTieBreakEnable(); } 
                else if ( _player1->getSets() == SETS_TO_WIN_MATCH ) {
                    _mode1WinSequences.p1MatchWinSequence();
                    _gameState->stopGameRunning();
                } else {     
                    _gameState->setPlayer1SetHistory( _player1->getSetHistory());
                    _gameState->setPlayer2SetHistory( _player2->getSetHistory());
                    _mode1WinSequences.p1SetWinSequence();  // call set win before incrementing set
                    _gameState->setCurrentSet( _gameState->getCurrentSet() + 1 ); // moved here sep4
                    _setLeds.updateSets();
                    GameTimer::gameDelay( _gameState->getWinDelay());
                    _resetGame(); }
                    _player1->setGames( 0 );
                    _player2->setGames( 0 );
            } else {    // no set win, no match win, no tie break. just a regular game win.
                std::cout << "*** calling p1GameWinSequence() ***" << std::endl;
                _gameLeds.updateGames();
                _gameState->setPlayer1SetHistory( _player1->getSetHistory());  // gamestate needs update here
                _gameState->setPlayer2SetHistory( _player2->getSetHistory());
                _mode1WinSequences.p1GameWinSequence();  // sets player points to zero
                _resetGame();
            }}
    } else {
        std::cout << "*** calling p1GameWinSequence() ***" << std::endl;
        _gameLeds.updateGames();
        _gameState->setPlayer1SetHistory( _player1->getSetHistory());
        _gameState->setPlayer2SetHistory( _player2->getSetHistory());
        _mode1WinSequences.p1GameWinSequence();
        _resetGame(); }}
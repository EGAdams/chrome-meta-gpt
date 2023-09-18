void Mode1Score::mode1P2Games() {
    _gameState->setServeSwitch( _gameState->getServeSwitch() + 1 );
    if ( _player2->getGames() >= GAMES_TO_WIN_SET ) {
        if ( _player2->getGames() == GAMES_TO_WIN_SET && _player1->getGames() == GAMES_TO_WIN_SET ) {
            _gameState->setTieBreak( 1 );
            _mode1TieBreaker.tieBreakEnable(); }
        if ( _gameState->getTieBreak() == 0 ) {
            if (( _player2->getGames() - _player1->getGames()) > 1 ) {
                _player2->setSets( _gameState, _player2->getSets() + 1 );
                _setLeds.updateSets();
                if ( _player2->getSets() == _player1->getSets()) {
                    _mode1WinSequences.p2TBSetWinSequence();
                    _gameState->setSetTieBreak( 1 );
                    _mode1TieBreaker.setTieBreakEnable(); }
                else if ( _player2->getSets() == SETS_TO_WIN_MATCH ) {
                    _mode1WinSequences.p2MatchWinSequence();
                    _gameState->stopGameRunning();
                } else {
                    _gameState->setPlayer1SetHistory( _player1->getSetHistory());
                    _gameState->setPlayer2SetHistory( _player2->getSetHistory());
                    _mode1WinSequences.p2SetWinSequence();
                    _gameState->setCurrentSet( _gameState->getCurrentSet() + 1 );
                    _setLeds.updateSets();
                    GameTimer::gameDelay( _gameState->getWinDelay());
                    _resetGame();
                    _player1->setGames( 0 );
                    _player2->setGames( 0 ); }}
                _player1->setGames( 0 );
                _player2->setGames( 0 );
            } else {
                std::cout << "inside mode1P2Games().  calling p2GameWinSequence()..." << std::endl;
                _gameLeds.updateGames();
                _gameState->setPlayer1SetHistory( _player1->getSetHistory());
                _gameState->setPlayer2SetHistory( _player2->getSetHistory());
                _gameState->setCurrentSet( _gameState->getCurrentSet() + 1 );
                _mode1WinSequences.p2GameWinSequence();
                _resetGame(); }
    } else {
        _gameLeds.updateGames();
        _mode1WinSequences.p2GameWinSequence();  // sets player points to zero
        _gameState->setPlayer1SetHistory( _player1->getSetHistory());
        _gameState->setPlayer2SetHistory( _player2->getSetHistory());
        _resetGame(); }}
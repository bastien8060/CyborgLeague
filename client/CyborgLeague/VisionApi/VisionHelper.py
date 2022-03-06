class Instance:
    def refresh(self, screen_elements):
        self.screen_elements = screen_elements

    def enemyBuildingsVisible(self) -> int:
        return len(self.screen_elements['buildings_points'])
    
    def enemyMinionsVisible(self) -> int:
        return len(self.screen_elements['minion_points'])

    def enemyChampionsVisible(self) -> int:
        return len(self.screen_elements['champion_points'])

    def enemyVisible(self) -> int:
        return self.enemyChampionsVisible() + self.enemyMinionsVisible()

    def allyMinionsVisible(self,attackTurret=False) -> int:
        advanced_minions = []
        for minion in self.screen_elements['ally_minion_points']:
            if minion[0] > 690 and (minion[1] < 380 or not attackTurret):
                advanced_minions.append(minion)
        return len(advanced_minions)

    def allyBuildingsVisible(self) -> int:
        return len(self.screen_elements['ally_buildings_points'])
    
    def allyChampionsVisible(self) -> int:
        return len(self.screen_elements['ally_champion_points'])

    def allyVisible(self) -> int:
        return self.allyChampionsVisible() + self.allyMinionsVisible()
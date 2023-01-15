--For this script credits to this video https://www.youtube.com/watch?v=xMhXAsqLJ9w
local API = require(game.ServerScriptService:WaitForChild("TrelloAPI"))
local BanBoardId = API:GetBoardID("Robloxbandatabase")
local BanListID = API:GetListID("Bans",BanBoardId)
local banmsg = 'You are banned from this game'



function checkCurrentPlayersforban()
	while wait(3) do
		local bancards = API:GetCardsInList(BanListID)
		for _, Player in pairs(game.Players:GetChildren()) do
			for _, Card in pairs(bancards) do
				if string.find(Card.name, Player.UserId) then
					Player:Kick(banmsg)
				end
			end
		end
	end
end

spawn(checkCurrentPlayersforban)

game.Players.PlayerAdded:Connect(function(plr)
	local bancards = API:GetCardsInList(BanListID)
	for _, Card in pairs(bancards) do
		if string.find(Card.name, plr.UserId) then
			plr:Kick(banmsg)
		end
	end
end)